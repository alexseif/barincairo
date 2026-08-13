import argparse
import asyncio
import sys

from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.exceptions import UserAlreadyExists

from app.core.database import AsyncSessionLocal
from app.core.users import UserManager
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def create_admin_user(email: str, password: str) -> None:
    async with AsyncSessionLocal() as session:
        user_db = SQLAlchemyUserDatabase(session, User)
        user_manager = UserManager(user_db)

        user_create = UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=True,
            is_verified=True,
        )

        try:
            user = await user_manager.create(user_create)
            print(f"Superuser successfully created: {user.email} (ID: {user.id})")
        except UserAlreadyExists:
            print(f"User with email '{email}' already exists. Updating credentials & superuser status...")
            user = await user_manager.get_by_email(email)
            user_update = UserUpdate(
                password=password,
                is_active=True,
                is_superuser=True,
                is_verified=True,
            )
            updated_user = await user_manager.update(user_update, user, safe=False)
            print(f"User '{updated_user.email}' updated with new password and superuser privileges.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bar in Cairo CLI Utilities")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    create_admin_parser = subparsers.add_parser(
        "create-admin", help="Create or upgrade a superuser account"
    )
    create_admin_parser.add_argument("--email", required=True, help="Superuser email address")
    create_admin_parser.add_argument("--password", required=True, help="Superuser password")

    args = parser.parse_args()

    if args.command == "create-admin":
        asyncio.run(create_admin_user(args.email, args.password))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
