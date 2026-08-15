from typing import Any, ClassVar

from sqladmin import BaseView, ModelView, expose
from sqladmin.filters import AllUniqueStringValuesFilter, BooleanFilter
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
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


class ScraperAdminView(BaseView):
    name = "Scrape Venues"
    icon = "fa-solid fa-compass"

    @expose("/scrape", methods=["GET", "POST"])
    async def scrape_venues_page(self, request: Request) -> Any:
        import os

        error_message = None
        info_message = None
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            error_message = "GOOGLE_MAPS_API_KEY is missing in your .env configuration. Please add your key to execute live extraction."

        if request.method == "POST":
            form = await request.form()
            location = form.get("location", "downtown")
            qty_raw = form.get("qty", "10")
            try:
                qty = int(qty_raw)
            except ValueError:
                qty = 10

            from scripts.extract_gmaps_venues import extract_and_stage_venues

            try:
                records = await extract_and_stage_venues(location=str(location), qty=qty)
                if records and len(records) > 0:
                    return RedirectResponse("/admin/venue-staging/list", status_code=303)
                else:
                    info_message = f"Extraction completed, but 0 new un-staged venues were found for location '{location}' (they may already exist in staging/production, or Google returned 0 results)."
            except Exception as exc:
                error_message = str(exc)

        alert_html = ""
        if error_message:
            alert_html = f'<div style="background:#fee2e2; border:1px solid #ef4444; color:#991b1b; padding:0.875rem 1rem; border-radius:6px; font-size:0.875rem; margin-bottom:1.25rem; font-weight:500;">⚠️ <strong>Extraction Error:</strong> {error_message}</div>'
        elif info_message:
            alert_html = f'<div style="background:#e0f2fe; border:1px solid #0284c7; color:#0369a1; padding:0.875rem 1rem; border-radius:6px; font-size:0.875rem; margin-bottom:1.25rem; font-weight:500;">ℹ️ {info_message}</div>'

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Scrape Venues - Bar in Cairo Admin</title>
            <style>
                body {{ font-family: system-ui, -apple-system, sans-serif; background: #ede7d8; color: #24332d; padding: 2rem; }}
                .card {{ background: #ffffff; padding: 2rem; border-radius: 8px; max-width: 520px; margin: 0 auto; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
                h1 {{ color: #24332d; font-size: 1.5rem; margin-bottom: 0.5rem; }}
                label {{ display: block; margin-top: 1rem; font-weight: 600; font-size: 0.875rem; }}
                input {{ width: 100%; padding: 0.5rem; margin-top: 0.25rem; border: 1px solid #b9ae96; border-radius: 4px; box-sizing: border-box; }}
                button {{ background: #24332d; color: #ffffff; padding: 0.625rem 1.25rem; border: none; border-radius: 4px; font-weight: 600; margin-top: 1.5rem; cursor: pointer; }}
                button:hover {{ background: #ad793b; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🔍 Extract & Stage Venues</h1>
                <p style="color: #657067; font-size: 0.875rem; margin-bottom: 1.25rem;">Enter a target Cairo area or district and maximum quantity to extract lightweight venue candidates into Venue Staging.</p>
                {alert_html}
                <form method="POST" action="/admin/scrape">
                    <label for="location">Target Area / District</label>
                    <input type="text" id="location" name="location" value="downtown" placeholder="e.g. heliopolis, downtown, maadi" required />
                    
                    <label for="qty">Max Quantity</label>
                    <input type="number" id="qty" name="qty" value="10" min="1" max="50" required />
                    
                    <button type="submit">Start Extraction</button>
                </form>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(html_content)


