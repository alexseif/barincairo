# Architectural Specification: Admin User Authentication

**Feature Goal**: Implement database-backed admin user authentication using `fastapi-users` with `SQLAlchemy` async ORM, `argon2`/`bcrypt` password hashing, absolute `.env` path resolution, and Starlette/SQLAdmin session cookie security compatible with local HTTP development (`http://localhost:8000/admin`) and production HTTPS (`SEC-1.1` to `SEC-1.5`).  
**Author**: `cairo-architect`  
**Date**: 2026-08-13  
**Status**: Draft  

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
  - Public user registration endpoints (admin access is strictly for system operators and content managers).
  - Modifications to spatial PostGIS models (`venues`, `categories`, `vibe_tags`).

### 1.2 Layered Architecture & Separation of Concerns
- **Backend Layering (FastAPI)**:
  - `API Routers & Auth Endpoints` (`backend/app/api/`): HTTP authentication routes (`/auth/jwt/login`, `/auth/jwt/logout`) generated via `fastapi-users`. Zero custom business logic.
  - `Service Layer` (`backend/app/core/users.py`): `UserManager` handling password hashing (`argon2`/`bcrypt`), password resets, and user lifecycle events.
  - `Repository / DAO Layer` (`backend/app/models/user.py`): SQLAlchemy `User` ORM entity extending `SQLAlchemyBaseUserTableUUID`. Zero request awareness.
- **Frontend / Admin Integration Layer**:
  - `SQLAdmin Integration` (`backend/app/admin/auth.py`): Custom `AdminAuth` adapter verifying credentials against `UserManager` with environment-aware session cookies (`same_site="lax"`, `https_only=False` for local dev).

---

## 2. Data Schema & Model Specifications

### 2.1 Database Models (PostGIS & PostgreSQL)
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

### 2.2 API Request/Response Payloads (Pydantic)
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

### 2.3 Frontend Type Definitions (TypeScript)
```typescript
export interface UserSession {
  id: string
  email: string
  is_active: boolean
  is_superuser: boolean
}
```

---

## 3. API Endpoint Contracts & Integration Specs

| Method | Endpoint Path | Description | Authentication / Access | Rate Limit |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login` | Obtain JWT access token | Public | 10 req/min |
| `POST` | `/api/v1/auth/logout` | Revoke session / JWT | Authenticated | 30 req/min |
| `GET` | `/admin` | SQLAdmin management dashboard | Admin Auth Session | Session Guard |

### 3.1 Session Authentication Adapter (`backend/app/admin/auth.py`)
```python
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

## 4. Zero-Trust Security & Design Compliance Checklist

- [ ] **SEC-1.1**: All incoming login and user creation payloads validated strictly via Pydantic schemas (`UserCreate`, `UserRead`).
- [ ] **SEC-1.2**: User database interactions use parameterized ORM queries with `argon2` or `bcrypt` password hashing.
- [ ] **SEC-1.3**: Admin email strings and username inputs sanitized prior to database persistence.
- [ ] **SEC-1.4**: Absolute `.env` path resolution configured (`Path(__file__).resolve().parents[3] / ".env"`), ensuring password updates in `.env` reflect immediately across all execution CWDs.
- [ ] **SEC-1.5**: Session cookies configured with `same_site="lax"`, `https_only=False` for local HTTP development (`http://localhost:8000/admin`), and `https_only=True` for production HTTPS.
- [ ] **Khedivial Matrix**: SQLAdmin custom CSS matches Khedivial color tokens (`#ede7d8`, `#24332d`, `#ad793b`).

---

## 5. Handoff & Developer Instructions

- **Target Files for `cairo-developer`**:
  - Model: `backend/app/models/user.py`
  - Schemas: `backend/app/schemas/user.py`
  - User Manager: `backend/app/core/users.py`
  - Configuration: `backend/app/core/config.py` (Absolute `.env` path fix)
  - Admin Adapter: `backend/app/admin/auth.py`
  - CLI Script: `backend/app/cli.py` (`python -m backend.app.cli create-admin`)
- **Verification Gate**: All Vitest and Pytest test suites must pass cleanly with 0 type errors (`"strict": true`) and 0 lint warnings. Verify login succeeds on local HTTP (`http://127.0.0.1:8000/admin`) with updated `.env` password.
