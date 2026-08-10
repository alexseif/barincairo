from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SubscriberCreate(BaseModel):
    whatsapp_number: str = Field(..., min_length=8, max_length=30, description="International phone format e.g. +201000000000")
    source: Optional[str] = "website"


class SubscriberResponse(BaseModel):
    id: int
    whatsapp_number: str
    source: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
