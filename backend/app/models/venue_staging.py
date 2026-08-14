import uuid
from datetime import datetime, timezone

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.venues import Base


class VenueStaging(Base):
    __tablename__ = "venue_staging"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    google_maps_url: Mapped[str] = mapped_column(Text, nullable=False)
    name_raw: Mapped[str] = mapped_column(String(255), nullable=False)
    address_raw: Mapped[str] = mapped_column(Text, nullable=False)
    working_hours: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location: Mapped[object] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=False,
    )
    raw_payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    enriched_payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="PENDING_CURATION", index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

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
        return f"<VenueStaging {self.place_id} status={self.status}>"

