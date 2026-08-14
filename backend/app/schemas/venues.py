from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    slug: str
    name: str


class CategoryResponse(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class VibeTagBase(BaseModel):
    slug: str
    name: str


class VibeTagResponse(VibeTagBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class GeoJSONGeometry(BaseModel):
    type: str = "Point"
    coordinates: list[float] = Field(..., description="[longitude, latitude]")


class VenueProperties(BaseModel):
    id: int
    slug: str
    name: str
    description: str | None = None
    address: str
    working_hours: str | None = None
    price_range: str = "$$"
    vibe_description: str | None = None
    photo_url: str | None = None
    category_slug: str
    category_name: str
    vibes: list[str] = []


class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: GeoJSONGeometry
    properties: VenueProperties


class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: list[GeoJSONFeature]
