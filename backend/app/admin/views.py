from typing import Any, ClassVar

from sqladmin import ModelView
from sqladmin.filters import AllUniqueStringValuesFilter, BooleanFilter
from wtforms import Field, FloatField, Form, validators

from app.models.subscribers import Subscriber
from app.models.user import User
from app.models.venue_staging import VenueStaging
from app.models.venues import Category, Venue, VenuePhoto, VibeTag


class UserAdmin(ModelView, model=User):
    column_list: ClassVar = ["id", "email", "is_active", "is_superuser", "is_verified", "created_at"]
    column_searchable_list: ClassVar = ["email"]
    column_filters: ClassVar = [
        BooleanFilter(User.is_active),
        BooleanFilter(User.is_superuser),
        BooleanFilter(User.is_verified),
    ]
    icon = "fa-solid fa-users"


class CategoryAdmin(ModelView, model=Category):
    column_list: ClassVar = [Category.id, Category.slug, Category.name]
    column_searchable_list: ClassVar = [Category.name, Category.slug]
    form_columns: ClassVar = ["slug", "name"]
    icon = "fa-solid fa-list"


class VibeTagAdmin(ModelView, model=VibeTag):
    column_list: ClassVar = [VibeTag.id, VibeTag.slug, VibeTag.name]
    column_searchable_list: ClassVar = [VibeTag.name, VibeTag.slug]
    form_columns: ClassVar = ["slug", "name"]
    icon = "fa-solid fa-tags"


class VenueAdmin(ModelView, model=Venue):
    column_list: ClassVar = [
        Venue.id,
        Venue.slug,
        Venue.name,
        Venue.category,
        Venue.address,
        Venue.working_hours,
        Venue.price_range,
        Venue.is_active,
    ]
    column_details_list: ClassVar = [
        Venue.id,
        Venue.slug,
        Venue.name,
        Venue.description,
        Venue.address,
        Venue.working_hours,
        Venue.google_maps_url,
        Venue.price_range,
        Venue.vibe_description,
        Venue.photo_url,
        Venue.is_active,
        Venue.category,
        Venue.vibes,
        Venue.photos,
    ]
    column_searchable_list: ClassVar = [Venue.name, Venue.slug, Venue.address]
    column_filters: ClassVar = [
        AllUniqueStringValuesFilter(Venue.price_range),
        BooleanFilter(Venue.is_active),
    ]
    form_columns: ClassVar = [
        "slug",
        "name",
        "description",
        "address",
        "working_hours",
        "google_maps_url",
        "price_range",
        "vibe_description",
        "photo_url",
        "is_active",
        "category",
        "vibes",
    ]
    icon = "fa-solid fa-martini-glass-citrus"

    async def scaffold_form(self, rules: list[str] | None = None) -> type[Form]:
        form_class = await super().scaffold_form(rules)
        form_class.latitude = FloatField("Latitude", validators=[validators.Optional()])
        form_class.longitude = FloatField("Longitude", validators=[validators.Optional()])
        return form_class

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Any) -> None:
        lat = data.pop("latitude", None)
        lng = data.pop("longitude", None)
        if lat is not None:
            model.latitude = float(lat)
        if lng is not None:
            model.longitude = float(lng)

    async def on_form_prefill(self, form: Any, model: Any) -> None:
        if hasattr(form, "latitude"):
            form.latitude.data = model.latitude
        if hasattr(form, "longitude"):
            form.longitude.data = model.longitude


class VenueStagingAdmin(ModelView, model=VenueStaging):
    column_list: ClassVar = [
        VenueStaging.id,
        VenueStaging.place_id,
        VenueStaging.name_raw,
        VenueStaging.address_raw,
        VenueStaging.working_hours,
        VenueStaging.status,
    ]
    column_searchable_list: ClassVar = [VenueStaging.name_raw, VenueStaging.place_id, VenueStaging.google_maps_url]
    column_filters: ClassVar = [AllUniqueStringValuesFilter(VenueStaging.status)]
    form_columns: ClassVar = [
        "place_id",
        "google_maps_url",
        "name_raw",
        "address_raw",
        "working_hours",
        "status",
        "raw_payload",
        "enriched_payload",
    ]
    form_args: ClassVar = {
        "raw_payload": {"validators": [validators.Optional()]},
        "enriched_payload": {"validators": [validators.Optional()]},
    }
    icon = "fa-solid fa-layer-group"

    async def scaffold_form(self, rules: list[str] | None = None) -> type[Form]:
        form_class = await super().scaffold_form(rules)
        form_class.latitude = FloatField("Latitude", validators=[validators.Optional()])
        form_class.longitude = FloatField("Longitude", validators=[validators.Optional()])
        return form_class

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Any) -> None:
        lat = data.pop("latitude", None)
        lng = data.pop("longitude", None)
        if lat is not None:
            model.latitude = float(lat)
        if lng is not None:
            model.longitude = float(lng)

    async def on_form_prefill(self, form: Any, model: Any) -> None:
        if hasattr(form, "latitude"):
            form.latitude.data = model.latitude
        if hasattr(form, "longitude"):
            form.longitude.data = model.longitude


class VenuePhotoAdmin(ModelView, model=VenuePhoto):
    column_list: ClassVar = [VenuePhoto.id, VenuePhoto.venue_id, VenuePhoto.photo_url, VenuePhoto.caption]
    form_columns: ClassVar = ["venue", "photo_url", "caption"]
    icon = "fa-solid fa-image"


class SubscriberAdmin(ModelView, model=Subscriber):
    column_list: ClassVar = [Subscriber.id, Subscriber.whatsapp_number, Subscriber.source, Subscriber.created_at]
    column_searchable_list: ClassVar = [Subscriber.whatsapp_number]
    form_columns: ClassVar = ["whatsapp_number", "source"]
    icon = "fa-solid fa-envelope"
