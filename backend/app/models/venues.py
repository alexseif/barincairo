from datetime import datetime, timezone

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
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
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    venues: Mapped[list["Venue"]] = relationship("Venue", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.slug}>"


class VibeTag(Base):
    __tablename__ = "vibe_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    venues: Mapped[list["Venue"]] = relationship("Venue", secondary=venue_vibes, back_populates="vibes")

    def __repr__(self) -> str:
        return f"<VibeTag {self.slug}>"


class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    google_maps_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[object] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=False,
    )
    price_range: Mapped[str] = mapped_column(String(10), default="$$", nullable=False)
    working_hours: Mapped[str | None] = mapped_column(String(100), nullable=True)
    vibe_description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    category: Mapped["Category"] = relationship("Category", back_populates="venues")
    vibes: Mapped[list["VibeTag"]] = relationship("VibeTag", secondary=venue_vibes, back_populates="venues")
    photos: Mapped[list["VenuePhoto"]] = relationship("VenuePhoto", back_populates="venue", cascade="all, delete-orphan")

    @property
    def latitude(self) -> float | None:
        if self.location is None:
            return None
        try:
            shape = to_shape(self.location)
            return float(shape.y)
        except Exception:
            return None

    @latitude.setter
    def latitude(self, val: float | None) -> None:
        if val is None:
            return
        lng = self.longitude if self.longitude is not None else 0.0
        self.location = WKTElement(f"POINT({lng} {val})", srid=4326)

    @property
    def longitude(self) -> float | None:
        if self.location is None:
            return None
        try:
            shape = to_shape(self.location)
            return float(shape.x)
        except Exception:
            return None

    @longitude.setter
    def longitude(self, val: float | None) -> None:
        if val is None:
            return
        lat = self.latitude if self.latitude is not None else 0.0
        self.location = WKTElement(f"POINT({val} {lat})", srid=4326)

    def __repr__(self) -> str:
        return f"<Venue {self.slug}>"


class VenuePhoto(Base):
    __tablename__ = "venue_photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    venue_id: Mapped[int] = mapped_column(Integer, ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(500), nullable=False)
    caption: Mapped[str | None] = mapped_column(String(255), nullable=True)

    venue: Mapped["Venue"] = relationship("Venue", back_populates="photos")

