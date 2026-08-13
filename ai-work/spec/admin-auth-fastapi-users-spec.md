# Architectural Specification: Admin User Authentication (`fastapi-users`)

**Document Path**: `ai-work/spec/admin-auth-fastapi-users-spec.md`  
**Feature Goal**: Integrate `fastapi-users` database authentication, `SQLAlchemy` async ORM user models, `argon2`/`bcrypt` password hashing, absolute `.env` path resolution, and local HTTP / production HTTPS cookie session management (`SEC-1.1` to `SEC-1.5`).  
**Author**: `cairo-architect`  
**Date**: 2026-08-13  
**Status**: Approved Specification  

---

## 1. Objective

Provide a robust, package-based admin user authentication system for `BARINCAIRO.COM` using `fastapi-users`. This resolves `.env` credential discovery issues, enables password changes in `.env`, secures admin password verification in PostgreSQL with `argon2`/`bcrypt` hashing, and supports local HTTP development (`http://localhost:8000/admin`) alongside production HTTPS.

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
    ...
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH) if ENV_FILE_PATH.exists() else ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
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
from app.core.config import settings

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({"token": "authenticated"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        return token == "authenticated"

authentication_backend = AdminAuth(
    secret_key=settings.SECRET_KEY,
)
```

---

## 4. Security (SEC-1.1 to SEC-1.5)

- [ ] **SEC-1.1**: Incoming user payloads parsed and validated using Pydantic schemas (`UserCreate`, `UserRead`).
- [ ] **SEC-1.2**: Password verification executed via parameterized ORM queries using `argon2`/`bcrypt` password hashing.
- [ ] **SEC-1.3**: Admin user input sanitized prior to database persistence.
- [ ] **SEC-1.4**: Absolute `.env` path resolution enforced (`ENV_FILE_PATH`), ensuring password edits in `.env` reflect across all execution environments.
- [ ] **SEC-1.5**: Session cookies configured with `same_site="lax"`, `https_only=False` for local HTTP dev (`http://localhost:8000/admin`), and `https_only=True` for production HTTPS.

---

## 5. Testing Strategy

- **Vitest**: Run `npm test -- --run` to verify frontend rendering and API mocks remain 100% passing.
- **Pytest / Integration**: Verify async FastAPI auth router endpoints (`/api/v1/auth/login`) and SQLAdmin login redirect handlers.
- **Manual Verification**: Verify successful login at `http://127.0.0.1:8000/admin` using updated `.env` password on local HTTP.

---

## 6. Handoff Instructions

1. **Implement User Model**: Create `User` table in `backend/app/models/user.py`.
2. **Implement Schemas**: Create Pydantic user schemas in `backend/app/schemas/user.py`.
3. **Configure Auth Manager**: Create `backend/app/core/users.py` and hook into `fastapi-users`.
4. **Update Configuration**: Fix `ENV_FILE_PATH` in `backend/app/core/config.py`.
5. **Update SQLAdmin Auth**: Wire `AdminAuth` in `backend/app/admin/auth.py`.
6. **Create CLI Tool**: Add `backend/app/cli.py` (`python -m backend.app.cli create-admin`).
7. **Verification**: Execute test harnesses and verify 0 type errors, 0 lint warnings.
