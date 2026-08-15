from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from app.models.base import Base, TimestampMixin


class User(SQLAlchemyBaseUserTableUUID, TimestampMixin, Base):
    __tablename__ = "users"

