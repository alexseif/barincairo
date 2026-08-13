from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SubscriberCreate(BaseModel):
    whatsapp_number: str = Field(..., min_length=8, max_length=30, description="International phone format e.g. +201000000000")
    source: str | None = "website"


class SubscriberResponse(BaseModel):
    id: int
    whatsapp_number: str
    source: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

