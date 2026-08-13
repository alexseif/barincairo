# Architectural Specification: Admin User Authentication (`fastapi-users`)

**Document Path**: `ai-work/spec/admin-auth-fastapi-users-spec.md`  
**Feature Goal**: Integrate `fastapi-users` database authentication, `SQLAlchemy` async ORM user models, `argon2`/`bcrypt` password hashing, absolute `.env` path resolution, and local HTTP / production HTTPS cookie session management (`SEC-1.1` to `SEC-1.5`).  
**Author**: `cairo-architect`  
**Date**: 2026-08-13  
**Status**: Approved Specification (DB Auth Only - Legacy `.env` Credentials Removed)  

---

## 1. Objective

Provide a robust, package-based admin user authentication system for `BARINCAIRO.COM` using `fastapi-users`. Plaintext `.env`-based admin authentication (`ADMIN_USERNAME` and `ADMIN_PASSWORD`) is completely deprecated and removed. All admin authentication is strictly backed by the database (`users` table) managed via `fastapi-users`. Absolute `.env` path resolution (`ENV_FILE_PATH`) ensures `DATABASE_URL` and `SECRET_KEY` load reliably across execution contexts, and session cookie configuration supports local HTTP development (`http://localhost:8000/admin`) alongside production HTTPS.

---

## 2. Scope & Boundaries

### 2.1 In-Scope Target Modules
- `backend/app/models/user.py`
- `backend/app/schemas/user.py`
- `backend/app/core/users.py`
- `backend/app/admin/auth.py`
- `backend/app/core/config.py`
- `backend/app/main.py`
- `backend/app/cli.py`

### 2.2 Out-of-Scope / Non-Goals
- Public end-user registration endpoints on the Next.js frontend (accounts are strictly for system administrators and content operators).
- Non-auth database schema changes to PostGIS spatial tables (`venues`, `categories`, `vibe_tags`).

---

## 3. Architecture & Schemas

### 3.1 Database User Model (`backend/app/models/user.py`)
```python
import uuid
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

### 3.2 Pydantic Validation Schemas (`backend/app/schemas/user.py`)
```python
import uuid
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
```

### 3.3 Configuration & Absolute `.env` Resolution (`backend/app/core/config.py`)
```python
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    PROJECT_NAME: str = "BARINCAIRO.COM API"
    VERSION: str = "1.3.0"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "postgresql+asyncpg://barincairo_user:change_me_in_env@db:5432/barincairo_db"
    SECRET_KEY: str = "change_me_in_env"
    # Legacy ADMIN_USERNAME and ADMIN_PASSWORD removed completely

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH) if ENV_FILE_PATH.exists() else ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
```

### 3.4 API Endpoints & Auth Adapter

| Method | Path | Description | Access | Rate Limit |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login` | JWT / Cookie Authentication Login | Public | 10 req/min |
| `POST` | `/api/v1/auth/logout` | Session Revocation | Authenticated | 30 req/min |
| `GET` | `/admin` | SQLAdmin Dashboard | Admin Auth Session | Session Guard |

```python
# backend/app/admin/auth.py
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from app.core.users import get_user_manager
from app.core.database import async_session_maker
from fastapi_users.exceptions import InvalidPasswordException, UserNotExists

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")  # email
        password = form.get("password")

        if not username or not password:
            return False

        async with async_session_maker() as session:
            # Authenticate via UserManager against database users
            ...
            if user and user.is_active and user.is_superuser:
                request.session.update({"user_id": str(user.id)})
                return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user_id")
        return bool(user_id)
```

---

## 4. Security (SEC-1.1 to SEC-1.5)

- [ ] **SEC-1.1**: Incoming user payloads parsed and validated using Pydantic schemas (`UserCreate`, `UserRead`).
- [ ] **SEC-1.2**: Password verification executed via parameterized ORM queries using `argon2`/`bcrypt` password hashing.
- [ ] **SEC-1.3**: Admin user input sanitized prior to database persistence.
- [ ] **SEC-1.4**: Absolute `.env` path resolution enforced (`ENV_FILE_PATH`), ensuring system settings (`DATABASE_URL`, `SECRET_KEY`) load reliably while removing legacy `.env` plaintext credentials (`ADMIN_USERNAME`/`ADMIN_PASSWORD`).
- [ ] **SEC-1.5**: Session cookies configured with `same_site="lax"`, `https_only=False` for local HTTP dev (`http://localhost:8000/admin`), and `https_only=True` for production HTTPS.

---

## 5. Testing Strategy

- **Pytest / Integration**: Verify async FastAPI auth router endpoints (`/api/v1/auth/login`), CLI user creation (`create-admin`), rejection of non-superusers, and SQLAdmin login redirect handlers.
- **Manual Verification**: Verify successful login at `http://127.0.0.1:8000/admin` using database superuser credentials on local HTTP.

---

## 6. Handoff Instructions

1. **Clean Config**: Update `backend/app/core/config.py` with `BASE_DIR`/`ENV_FILE_PATH` and remove `ADMIN_USERNAME`/`ADMIN_PASSWORD`.
2. **Implement User Model & Migration**: Create `User` table in `backend/app/models/user.py` and run Alembic migration.
3. **Implement Schemas & Auth Manager**: Create `backend/app/schemas/user.py` and `backend/app/core/users.py` with `fastapi-users`.
4. **Update SQLAdmin Auth**: Wire `AdminAuth` in `backend/app/admin/auth.py` to authenticate against database superusers.
5. **Create CLI Tool**: Add `backend/app/cli.py` (`python -m app.cli create-admin`).
6. **Verification**: Run `pytest`, `ruff check`, `mypy`.
