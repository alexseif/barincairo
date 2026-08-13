
from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    slug: str
    name_en: str
    name_ar: str


class CategoryResponse(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class VibeTagBase(BaseModel):
    slug: str
    name_en: str
    name_ar: str


class VibeTagResponse(VibeTagBase):
    id: int
    model_config = ConfigDict(from_attributes=True)



class GeoJSONGeometry(BaseModel):
    type: str = "Point"
    coordinates: list[float] = Field(..., description="[longitude, latitude]")


class VenueProperties(BaseModel):
    id: int
    slug: str
    name_en: str
    name_ar: str
    description_en: str | None = None
    description_ar: str | None = None
    address_en: str
    address_ar: str
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
