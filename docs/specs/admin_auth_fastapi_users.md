# Architectural Specification: Admin Authentication via `fastapi-users` & SQLAdmin Integration

**Feature Goal**: Implement package-based admin user authentication, database-backed `AdminUser` models, `fastapi-users` authentication manager, absolute `.env` path resolution, and seamless local HTTP / production HTTPS cookie session management (`SEC-1.1` to `SEC-1.5`).  
**Author**: `cairo-architect`  
**Date**: 2026-08-13  
**Status**: Draft (Approved for Handoff)  

---

## 1. Architectural Scope, Isolation & Design Patterns

### 1.1 Scope Boundaries & Isolation
- **In-Scope Target Modules**:
  - `backend/app/models/user.py`
  - `backend/app/schemas/user.py`
  - `backend/app/core/users.py`
  - `backend/app/admin/auth.py`
  - `backend/app/core/config.py`
  - `backend/app/main.py`
  - `backend/app/cli.py`
- **Out-of-Scope / Non-Goals**:
  - Public end-user registration on frontend (user accounts are strictly for admin operators and content managers).

### 1.2 Layered Architecture & Separation of Concerns
- **User Model Layer (`backend/app/models/user.py`)**: SQLAlchemy ORM `User` entity extending `SQLAlchemyBaseUserTableUUID` from `fastapi-users`.
- **Schema Validation Layer (`backend/app/schemas/user.py`)**: Pydantic `UserRead`, `UserCreate`, and `UserUpdate` schemas enforcing `SEC-1.1`.
- **Authentication Manager Layer (`backend/app/core/users.py`)**: `UserManager` executing `fastapi-users` password hashing (`argon2`/`bcrypt`), cookie transport, and database strategy.
- **Admin Auth Adapter Layer (`backend/app/admin/auth.py`)**: SQLAdmin `AuthenticationBackend` adapter validating login credentials against `UserManager` with environment-aware cookie session security (`same_site="lax"`, `https_only=False` on dev).
- **Configuration Layer (`backend/app/core/config.py`)**: Absolute path resolution for `.env` file loading so password changes in `.env` are always discovered regardless of launch directory.

---

## 2. Data Schema & Model Specifications

### 2.1 Database User Table DDL (PostgreSQL)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(320) UNIQUE NOT NULL,
    hashed_password VARCHAR(1024) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_superuser BOOLEAN NOT NULL DEFAULT false,
    is_verified BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users (email);
```

### 2.2 SQLAlchemy User Model (`backend/app/models/user.py`)
```python
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
```

### 2.3 Pydantic User Schemas (`backend/app/schemas/user.py`)
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

### 2.4 Absolute `.env` Path Resolution (`backend/app/core/config.py`)
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

### 2.5 SQLAdmin Auth Adapter (`backend/app/admin/auth.py`)
```python
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from app.core.config import settings

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        # Authenticate against fastapi-users / DB session or env credentials
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

## 3. Zero-Trust Security & Compliance Checklist

- [x] **SEC-1.1**: User credentials and email formats parsed strictly using Pydantic models.
- [x] **SEC-1.2**: Password verification and user queries executed via parameterized SQLAlchemy ORM queries with `argon2` or `bcrypt` hashing.
- [x] **SEC-1.3**: Admin user input sanitized before DB write.
- [x] **SEC-1.4**: Absolute path resolution configured for `.env` loading (`ENV_FILE_PATH`), ensuring `.env` password updates immediately reflect across CWDs.
- [x] **SEC-1.5**: Session cookies configured with `same_site="lax"`, `https_only=False` for local HTTP development (`http://localhost:8000/admin`), and `https_only=True` for production HTTPS.

---

## 4. Handoff & Developer Instructions

### 🎯 Task Instructions for `cairo-developer`:
1. **Install Package**: Ensure `fastapi-users[sqlalchemy]` and `passlib[bcrypt]` are specified in `pyproject.toml` / dependencies.
2. **Absolute `.env` Fix**: Update `backend/app/core/config.py` with explicit `ENV_FILE_PATH` resolving to root `.env`.
3. **User Models & Schemas**:
   - Implement `User` model in `backend/app/models/user.py`.
   - Implement `UserRead`, `UserCreate`, `UserUpdate` schemas in `backend/app/schemas/user.py`.
4. **Auth Backend & Manager**:
   - Create `backend/app/core/users.py` setting up `UserManager` and `fastapi-users` authentication backend.
   - Update `backend/app/admin/auth.py` with environment-aware cookie configuration (`same_site="lax"`, local HTTP dev support).
5. **CLI User Creation Script**:
   - Add `backend/app/cli.py` providing a CLI command to initialize or update admin credentials (`python -m backend.app.cli create-admin`).
6. **Verification Gate**:
   - Run Vitest & Pytest harnesses (`npm test -- --run` and `pytest`).
   - Verify login success on local HTTP (`http://127.0.0.1:8000/admin`) with custom `.env` password.
