from typing import ClassVar

from sqladmin import ModelView
from sqladmin.filters import AllUniqueStringValuesFilter, BooleanFilter

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
    column_list: ClassVar = [Category.id, Category.slug, Category.name_en, Category.name_ar]
    column_searchable_list: ClassVar = [Category.name_en, Category.slug]
    icon = "fa-solid fa-list"


class VibeTagAdmin(ModelView, model=VibeTag):
    column_list: ClassVar = [VibeTag.id, VibeTag.slug, VibeTag.name_en, VibeTag.name_ar]
    column_searchable_list: ClassVar = [VibeTag.name_en, VibeTag.slug]
    icon = "fa-solid fa-tags"


class VenueAdmin(ModelView, model=Venue):
    column_list: ClassVar = [
        Venue.id,
        Venue.slug,
        Venue.name_en,
        Venue.price_range,
        Venue.is_active,
        Venue.created_at,
    ]
    column_searchable_list: ClassVar = [Venue.name_en, Venue.slug, Venue.address_en]
    column_filters: ClassVar = [
        AllUniqueStringValuesFilter(Venue.price_range),
        BooleanFilter(Venue.is_active),
    ]
    icon = "fa-solid fa-martini-glass-citrus"


class VenueStagingAdmin(ModelView, model=VenueStaging):
    column_list: ClassVar = [
        VenueStaging.id,
        VenueStaging.place_id,
        VenueStaging.name_raw,
        VenueStaging.google_maps_url,
        VenueStaging.status,
        VenueStaging.created_at,
    ]
    column_searchable_list: ClassVar = [VenueStaging.name_raw, VenueStaging.place_id, VenueStaging.google_maps_url]
    column_filters: ClassVar = [AllUniqueStringValuesFilter(VenueStaging.status)]
    icon = "fa-solid fa-layer-group"


class VenuePhotoAdmin(ModelView, model=VenuePhoto):
    column_list: ClassVar = [VenuePhoto.id, VenuePhoto.venue_id, VenuePhoto.photo_url]
    icon = "fa-solid fa-image"


class SubscriberAdmin(ModelView, model=Subscriber):
    column_list: ClassVar = [Subscriber.id, Subscriber.whatsapp_number, Subscriber.source, Subscriber.created_at]
    column_searchable_list: ClassVar = [Subscriber.whatsapp_number]
    icon = "fa-solid fa-envelope"
