import re
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, HttpUrl

# Price Range Enum/Literal standard
PriceRange = Literal["$", "$$", "$$$", "$$$$"]

SLUG_PATTERN = r"^[a-z0-9-]+$"


class CategoryBase(BaseModel):
    slug: str = Field(
        ...,
        min_length=1,
        max_length=50,
        pattern=SLUG_PATTERN,
        description="Unique URL-friendly slug",
        examples=["bars"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Category display name",
        examples=["Bars & Pubs"],
    )

    model_config = ConfigDict(str_strip_whitespace=True)


class CategoryResponse(CategoryBase):
    id: int = Field(..., description="Primary key ID")
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class VibeTagBase(BaseModel):
    slug: str = Field(
        ...,
        min_length=1,
        max_length=50,
        pattern=SLUG_PATTERN,
        description="Unique URL-friendly vibe tag slug",
        examples=["cozy"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Vibe tag display name",
        examples=["Cozy"],
    )

    model_config = ConfigDict(str_strip_whitespace=True)


class VibeTagResponse(VibeTagBase):
    id: int = Field(..., description="Primary key ID")
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class GeoJSONGeometry(BaseModel):
    type: Literal["Point"] = Field(default="Point", description="GeoJSON geometry type")
    coordinates: list[float] = Field(..., description="[longitude, latitude]")

    @field_validator("coordinates")
    @classmethod
    def validate_coordinates(cls, v: list[float]) -> list[float]:
        if len(v) != 2:
            raise ValueError("GeoJSON Point coordinates must contain exactly 2 elements: [longitude, latitude]")
        lng, lat = v[0], v[1]
        if not (-180.0 <= lng <= 180.0):
            raise ValueError(f"Longitude must be between -180.0 and 180.0, got {lng}")
        if not (-90.0 <= lat <= 90.0):
            raise ValueError(f"Latitude must be between -90.0 and 90.0, got {lat}")
        return v


class VenueProperties(BaseModel):
    id: int = Field(..., description="Venue primary key ID")
    slug: str = Field(..., min_length=1, max_length=100, pattern=SLUG_PATTERN, description="Unique venue slug")
    name: str = Field(..., min_length=1, max_length=150, description="Venue name")
    description: str | None = Field(default=None, max_length=2000, description="Detailed description")
    address: str = Field(..., min_length=1, max_length=255, description="Physical address")
    working_hours: str | None = Field(default=None, max_length=100, description="Working hours description")
    price_range: PriceRange = Field(default="$$", description="Price level indicator")
    vibe_description: str | None = Field(default=None, max_length=255, description="Short vibe summary")
    photo_url: str | None = Field(default=None, description="Primary photo URL")
    category_slug: str = Field(..., min_length=1, max_length=50, description="Category slug")
    category_name: str = Field(..., min_length=1, max_length=100, description="Category display name")
    vibes: list[str] = Field(default_factory=list, description="List of associated vibe tag slugs")

    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True)


class GeoJSONFeature(BaseModel):
    type: Literal["Feature"] = Field(default="Feature", description="GeoJSON feature type")
    geometry: GeoJSONGeometry
    properties: VenueProperties


class GeoJSONFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = Field(default="FeatureCollection", description="GeoJSON collection type")
    features: list[GeoJSONFeature] = Field(default_factory=list, description="List of GeoJSON features")


class VenueCreate(BaseModel):
    """Schema for creating a new Venue."""

    slug: str = Field(..., min_length=1, max_length=100, pattern=SLUG_PATTERN, description="Unique venue slug")
    name: str = Field(..., min_length=1, max_length=150, description="Venue name")
    description: str | None = Field(default=None, max_length=2000, description="Detailed description")
    address: str = Field(..., min_length=1, max_length=255, description="Physical address")
    google_maps_url: str | None = Field(default=None, description="Google Maps URL")
    category_id: int = Field(..., gt=0, description="Associated Category ID")
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude coordinate")
    price_range: PriceRange = Field(default="$$", description="Price range ($, $$, $$$, $$$$)")
    working_hours: str | None = Field(default=None, max_length=100, description="Working hours")
    vibe_description: str | None = Field(default=None, max_length=255, description="Vibe description")
    photo_url: str | None = Field(default=None, description="Main photo URL")
    vibe_ids: list[int] = Field(default_factory=list, description="Associated vibe tag IDs")

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)


class VenueUpdate(BaseModel):
    """Schema for partial updates to a Venue."""

    slug: str | None = Field(default=None, min_length=1, max_length=100, pattern=SLUG_PATTERN)
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    address: str | None = Field(default=None, min_length=1, max_length=255)
    google_maps_url: str | None = Field(default=None)
    category_id: int | None = Field(default=None, gt=0)
    latitude: float | None = Field(default=None, ge=-90.0, le=90.0)
    longitude: float | None = Field(default=None, ge=-180.0, le=180.0)
    price_range: PriceRange | None = Field(default=None)
    working_hours: str | None = Field(default=None, max_length=100)
    vibe_description: str | None = Field(default=None, max_length=255)
    photo_url: str | None = Field(default=None)
    vibe_ids: list[int] | None = Field(default=None)
    is_active: bool | None = Field(default=None)

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
