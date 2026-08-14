from typing import Literal

from pydantic import BaseModel, Field, field_validator


class VenueIngestSchema(BaseModel):
    slug: str
    category_slug: str
    name: str
    description: str | None = None
    address: str
    working_hours: str | None = None
    google_maps_url: str
    latitude: float = Field(
        ...,
        ge=30.0380,
        le=30.0520,
        description="Latitude strictly within Downtown Cairo bounding box (30.0380 - 30.0520)",
    )
    longitude: float = Field(
        ...,
        ge=31.2300,
        le=31.2480,
        description="Longitude strictly within Downtown Cairo bounding box (31.2300 - 31.2480)",
    )
    price_range: Literal["$", "$$", "$$$"] = "$$"
    vibe_description: str | None = None
    photo_url: str
    gallery_photos: list[str] = Field(default_factory=list)
    vibes: list[str] = Field(default_factory=list)
    citations: list[str] = Field(
        ...,
        min_length=2,
        description="2-Citation Verification Gate (at least 2 verified sources/citations required)",
    )

    @field_validator("google_maps_url")
    @classmethod
    def validate_google_maps_url(cls, v: str) -> str:
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError("google_maps_url must be a valid HTTP/HTTPS URL")
        return v
