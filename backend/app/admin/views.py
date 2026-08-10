from sqladmin import ModelView
from app.models.subscribers import Subscriber
from app.models.venues import Category, Venue, VenuePhoto, VibeTag


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.slug, Category.name_en, Category.name_ar]
    column_searchable_list = [Category.name_en, Category.slug]
    icon = "fa-solid fa-list"


class VibeTagAdmin(ModelView, model=VibeTag):
    column_list = [VibeTag.id, VibeTag.slug, VibeTag.name_en, VibeTag.name_ar]
    column_searchable_list = [VibeTag.name_en, VibeTag.slug]
    icon = "fa-solid fa-tags"


class VenueAdmin(ModelView, model=Venue):
    column_list = [
        Venue.id,
        Venue.slug,
        Venue.name_en,
        Venue.price_range,
        Venue.is_active,
        Venue.created_at,
    ]
    column_searchable_list = [Venue.name_en, Venue.slug, Venue.address_en]
    column_filters = [Venue.price_range, Venue.is_active]
    icon = "fa-solid fa-martini-glass-citrus"


class VenuePhotoAdmin(ModelView, model=VenuePhoto):
    column_list = [VenuePhoto.id, VenuePhoto.venue_id, VenuePhoto.photo_url]
    icon = "fa-solid fa-image"


class SubscriberAdmin(ModelView, model=Subscriber):
    column_list = [Subscriber.id, Subscriber.whatsapp_number, Subscriber.source, Subscriber.created_at]
    column_searchable_list = [Subscriber.whatsapp_number]
    icon = "fa-solid fa-envelope"
