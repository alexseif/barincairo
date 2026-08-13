import uuid

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.core.users import UserManager
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.db import SQLAlchemyUserDatabase
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from starlette.requests import Request


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if not username or not password:
            return False

        credentials = OAuth2PasswordRequestForm(
            username=str(username),
            password=str(password),
            scope="",
            grant_type="password",
        )

        async with AsyncSessionLocal() as session:
            user_db: SQLAlchemyUserDatabase[User, uuid.UUID] = SQLAlchemyUserDatabase(session, User)
            user_manager = UserManager(user_db)
            user = await user_manager.authenticate(credentials)

            if user and user.is_active and user.is_superuser:
                request.session.update({"token": str(user.id)})
                return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        try:
            user_id = uuid.UUID(token)
        except ValueError:
            request.session.clear()
            return False

        async with AsyncSessionLocal() as session:
            stmt = select(User).where(
                User.id == user_id,  # type: ignore[arg-type]
                User.is_active,  # type: ignore[arg-type]
                User.is_superuser,  # type: ignore[arg-type]
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                return True

        request.session.clear()
        return False


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
