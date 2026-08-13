# Task List: Admin User Authentication (`fastapi-users`)

- [x] **Task 1: Dependencies & Absolute `.env` Config Cleanup (`SEC-1.4`)**
  - Add `fastapi-users[sqlalchemy]` and `argon2-cffi` to `backend/requirements.txt`
  - Update `backend/app/core/config.py` with `BASE_DIR` & `ENV_FILE_PATH` absolute resolution
  - Remove legacy `ADMIN_USERNAME` and `ADMIN_PASSWORD` from `config.py` (removing `.env` auth)
  - Verification: `python -c "from app.core.config import settings; print(hasattr(settings, 'ADMIN_PASSWORD'))"`

- [x] **Task 2: Database User Model & Alembic Migration (`SEC-1.2`)**
  - Create `User` model in `backend/app/models/user.py` subclassing `SQLAlchemyBaseUserTableUUID`
  - Expose `User` in `backend/app/models/__init__.py`
  - Generate and apply Alembic migration for `users` table
  - Verification: `alembic check` and DB table reflection check

- [x] **Task 3: Pydantic Schemas & `fastapi-users` Core Setup (`SEC-1.1`, `SEC-1.2`, `SEC-1.3`)**
  - Create `UserRead`, `UserCreate`, `UserUpdate` in `backend/app/schemas/user.py`
  - Create `backend/app/core/users.py` with `UserManager`, DB strategy, password hashing, and transports
  - Verification: Test instantiation of `UserManager` and password hashing functionality

- [x] **Task 4: API Auth Routers & SQLAdmin Database Auth Integration (`SEC-1.5`)**
  - Register `/api/v1/auth` routers in `backend/app/main.py`
  - Rewrite `AdminAuth` in `backend/app/admin/auth.py` to authenticate form credentials strictly against database superusers via `fastapi-users` `UserManager`
  - Verification: Test endpoint response for `/api/v1/auth/login` and SQLAdmin login with DB credentials

- [x] **Task 5: Admin Bootstrap CLI Tool**
  - Create `backend/app/cli.py` with `create-admin` command using `UserManager` to seed initial superuser in PostgreSQL
  - Verification: `python -m app.cli create-admin --help`

- [x] **Task 6: Integration Test Suite & System Verification**
  - Create `backend/tests/test_auth.py` covering database login, password hashing, rejection of legacy env auth, and SQLAdmin guard
  - Verification: Run `pytest`, `ruff check backend`, `mypy backend/app`
