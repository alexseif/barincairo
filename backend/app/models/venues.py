from datetime import datetime, timezone
from typing import List, Optional
from geoalchemy2 import Geometry
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Text, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# Many-to-Many Junction Table for Venues and Vibe Tags
venue_vibes = Table(
    "venue_vibes",
    Base.metadata,
    Column("venue_id", Integer, ForeignKey("venues.id", ondelete="CASCADE"), primary_key=True),
    Column("vibe_id", Integer, ForeignKey("vibe_tags.id", ondelete="CASCADE"), primary_key=True),
)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)

    venues: Mapped[List["Venue"]] = relationship("Venue", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.slug}>"


class VibeTag(Base):
    __tablename__ = "vibe_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)

    venues: Mapped[List["Venue"]] = relationship("Venue", secondary=venue_vibes, back_populates="vibes")

    def __repr__(self) -> str:
        return f"<VibeTag {self.slug}>"


class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    name_en: Mapped[str] = mapped_column(String(150), nullable=False)
    name_ar: Mapped[str] = mapped_column(String(150), nullable=False)
    description_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description_ar: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address_en: Mapped[str] = mapped_column(String(255), nullable=False)
    address_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[object] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=False,
    )
    price_range: Mapped[str] = mapped_column(String(10), default="$$", nullable=False)
    vibe_description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    photo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    category: Mapped["Category"] = relationship("Category", back_populates="venues")
    vibes: Mapped[List["VibeTag"]] = relationship("VibeTag", secondary=venue_vibes, back_populates="venues")
    photos: Mapped[List["VenuePhoto"]] = relationship("VenuePhoto", back_populates="venue", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Venue {self.slug}>"


class VenuePhoto(Base):
    __tablename__ = "venue_photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    venue_id: Mapped[int] = mapped_column(Integer, ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(500), nullable=False)
    caption: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    venue: Mapped["Venue"] = relationship("Venue", back_populates="photos")
