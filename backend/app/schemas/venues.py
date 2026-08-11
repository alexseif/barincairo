from typing import List, Optional
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
    coordinates: List[float] = Field(..., description="[longitude, latitude]")


class VenueProperties(BaseModel):
    id: int
    slug: str
    name_en: str
    name_ar: str
    description_en: Optional[str] = None
    description_ar: Optional[str] = None
    address_en: str
    address_ar: str
    price_range: str = "$$"
    vibe_description: Optional[str] = None
    photo_url: Optional[str] = None
    category_slug: str
    category_name: str
    vibes: List[str] = []


class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: GeoJSONGeometry
    properties: VenueProperties


class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]
