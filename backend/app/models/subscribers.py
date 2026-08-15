from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Subscriber(TimestampMixin, Base):
    __tablename__ = "subscribers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    whatsapp_number: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    source: Mapped[str | None] = mapped_column(String(50), default="website", nullable=True)

    def __repr__(self) -> str:
        return f"<Subscriber {self.whatsapp_number}>"
