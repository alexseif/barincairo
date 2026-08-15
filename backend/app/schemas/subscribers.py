from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SubscriberCreate(BaseModel):
    name: str | None = Field(None, max_length=100)
    whatsapp_number: str | None = Field(None, max_length=30, description="International phone format e.g. +201000000000")
    email: str | None = Field(None, max_length=255)
    source: str | None = "website"

    @model_validator(mode="after")
    def validate_contact(self) -> "SubscriberCreate":
        wa = (self.whatsapp_number or "").strip()
        em = (self.email or "").strip()
        if not wa and not em:
            raise ValueError("At least WhatsApp number or Email must be provided")
        if wa and len(wa) < 8:
            raise ValueError("WhatsApp number must be at least 8 characters long")
        return self


class SubscriberResponse(BaseModel):
    id: int
    name: str | None = None
    whatsapp_number: str | None = None
    email: str | None = None
    source: str | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

