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

    async def get_form_data_for_edit(self, obj: Any) -> dict[str, Any]:
        data = await super().get_form_data_for_edit(obj)
        data["latitude"] = getattr(obj, "latitude", None)
        data["longitude"] = getattr(obj, "longitude", None)
        return data

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Any) -> None:
        from geoalchemy2.elements import WKTElement
        lat_val = data.pop("latitude", None)
        lng_val = data.pop("longitude", None)

        existing_lat = getattr(model, "latitude", None)
        existing_lng = getattr(model, "longitude", None)

        lat = float(lat_val) if lat_val not in (None, "") else existing_lat
        lng = float(lng_val) if lng_val not in (None, "") else existing_lng

        if lat is not None and lng is not None:
            model.location = WKTElement(f"POINT({lng} {lat})", srid=4326)


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

    async def get_form_data_for_edit(self, obj: Any) -> dict[str, Any]:
        data = await super().get_form_data_for_edit(obj)
        data["latitude"] = getattr(obj, "latitude", None)
        data["longitude"] = getattr(obj, "longitude", None)
        return data

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Any) -> None:
        from geoalchemy2.elements import WKTElement
        lat_val = data.pop("latitude", None)
        lng_val = data.pop("longitude", None)

        existing_lat = getattr(model, "latitude", None)
        existing_lng = getattr(model, "longitude", None)

        lat = float(lat_val) if lat_val not in (None, "") else existing_lat
        lng = float(lng_val) if lng_val not in (None, "") else existing_lng

        if lat is not None and lng is not None:
            model.location = WKTElement(f"POINT({lng} {lat})", srid=4326)


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


class AddVenueFromUrlAdminView(BaseView):
    name = "Add Venue from URL"
    icon = "fa-solid fa-map-location-dot"

    @expose("/add-venue-url", methods=["GET", "POST"])
    async def add_venue_from_url_page(self, request: Request) -> Any:
        from sqlalchemy import select
        from geoalchemy2.elements import WKTElement
        from app.core.database import AsyncSessionLocal
        from app.core.gmaps_parser import parse_google_maps_url, slugify

        error_message = None
        form_data = await request.form() if request.method == "POST" else {}
        action = form_data.get("action")

        # Step 3: Handle Venue Creation & Save
        if request.method == "POST" and action == "save":
            try:
                name = str(form_data.get("name", "")).strip()
                slug = str(form_data.get("slug", "")).strip()
                address = str(form_data.get("address", "")).strip()
                gmaps_url = str(form_data.get("google_maps_url", "")).strip()
                lat = float(form_data.get("latitude", 30.0444))
                lng = float(form_data.get("longitude", 31.2357))
                category_id = int(form_data.get("category_id", 1))
                price_range = str(form_data.get("price_range", "$$")).strip()
                working_hours = str(form_data.get("working_hours", "")).strip() or None
                vibe_description = str(form_data.get("vibe_description", "")).strip() or None
                description = str(form_data.get("description", "")).strip() or None
                photo_url = str(form_data.get("photo_url", "")).strip() or None
                vibe_ids = [int(v) for v in form_data.getlist("vibe_ids")]

                async with AsyncSessionLocal() as session:
                    base_slug = slugify(slug or name) or "venue"
                    cur_slug = base_slug
                    counter = 1
                    while True:
                        res = await session.execute(select(Venue).where(Venue.slug == cur_slug))
                        if not res.scalar_one_or_none():
                            break
                        cur_slug = f"{base_slug}-{counter}"
                        counter += 1

                    new_venue = Venue(
                        name=name,
                        slug=cur_slug,
                        address=address,
                        google_maps_url=gmaps_url or None,
                        location=WKTElement(f"POINT({lng} {lat})", srid=4326),
                        category_id=category_id,
                        price_range=price_range,
                        working_hours=working_hours,
                        vibe_description=vibe_description,
                        description=description,
                        photo_url=photo_url,
                        is_active=True,
                    )

                    if vibe_ids:
                        vibe_res = await session.execute(select(VibeTag).where(VibeTag.id.in_(vibe_ids)))
                        new_venue.vibes = list(vibe_res.scalars().all())

                    session.add(new_venue)
                    await session.commit()
                    return RedirectResponse("/admin/venue/list", status_code=303)
            except Exception as exc:
                error_message = f"Failed to save venue: {str(exc)}"

        # Step 2: Handle URL Parsing & Render Pre-filled Edit Form
        url_input = str(form_data.get("url", "")).strip() if request.method == "POST" else request.query_params.get("url", "").strip()
        parsed_data = None

        if url_input and (action == "fetch" or request.method == "POST"):
            try:
                parsed_data = await parse_google_maps_url(url_input)
            except Exception as exc:
                error_message = f"Failed to parse Google Maps URL: {str(exc)}"

        # Load categories and vibes from DB for the form
        async with AsyncSessionLocal() as session:
            cat_res = await session.execute(select(Category).order_by(Category.name))
            categories = cat_res.scalars().all()
            vibe_res = await session.execute(select(VibeTag).order_by(VibeTag.name))
            vibes = vibe_res.scalars().all()

        alert_html = ""
        if error_message:
            alert_html = f'<div style="background:#fee2e2; border:1px solid #ef4444; color:#991b1b; padding:0.875rem 1rem; border-radius:6px; font-size:0.875rem; margin-bottom:1.25rem; font-weight:500;">⚠️ {error_message}</div>'

        # Render Form 1: Input Google Maps URL
        if not parsed_data:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Add Venue from Google Maps URL - Bar in Cairo Admin</title>
                <style>
                    body {{ font-family: system-ui, -apple-system, sans-serif; background: #ede7d8; color: #24332d; padding: 2rem; }}
                    .card {{ background: #ffffff; padding: 2rem; border-radius: 8px; max-width: 580px; margin: 0 auto; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
                    h1 {{ color: #24332d; font-size: 1.5rem; margin-bottom: 0.5rem; }}
                    label {{ display: block; margin-top: 1rem; font-weight: 600; font-size: 0.875rem; }}
                    input[type="text"], input[type="url"] {{ width: 100%; padding: 0.625rem; margin-top: 0.25rem; border: 1px solid #b9ae96; border-radius: 4px; box-sizing: border-box; }}
                    button {{ background: #24332d; color: #ffffff; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; font-weight: 600; margin-top: 1.5rem; cursor: pointer; width: 100%; font-size: 0.9375rem; }}
                    button:hover {{ background: #ad793b; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>📍 Add Venue from Google Maps URL</h1>
                    <p style="color: #657067; font-size: 0.875rem; margin-bottom: 1.25rem;">Paste a standard or short Google Maps link (e.g. <code>https://maps.app.goo.gl/...</code> or <code>https://www.google.com/maps/place/...</code>) to extract metadata and create a new venue.</p>
                    {alert_html}
                    <form method="POST" action="/admin/add-venue-url">
                        <input type="hidden" name="action" value="fetch" />
                        <label for="url">Google Maps URL</label>
                        <input type="url" id="url" name="url" placeholder="https://maps.app.goo.gl/..." required value="{url_input}" />
                        <button type="submit">Fetch Venue Metadata</button>
                    </form>
                </div>
            </body>
            </html>
            """
            return HTMLResponse(html_content)

        # Render Form 2: Preview & Edit Metadata before Save
        cat_options = "".join([f'<option value="{c.id}">{c.name}</option>' for c in categories])
        vibe_checkboxes = "".join([
            f'<label style="display:inline-flex; align-items:center; gap:0.375rem; font-weight:normal; margin-right:1rem; margin-top:0.375rem;"><input type="checkbox" name="vibe_ids" value="{v.id}"> {v.name}</label>'
            for v in vibes
        ])

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Review Venue Metadata - Bar in Cairo Admin</title>
            <style>
                body {{ font-family: system-ui, -apple-system, sans-serif; background: #ede7d8; color: #24332d; padding: 2rem; }}
                .card {{ background: #ffffff; padding: 2rem; border-radius: 8px; max-width: 680px; margin: 0 auto; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
                h1 {{ color: #24332d; font-size: 1.5rem; margin-bottom: 0.5rem; }}
                .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }}
                label {{ display: block; margin-top: 0.875rem; font-weight: 600; font-size: 0.875rem; color: #24332d; }}
                input, select, textarea {{ width: 100%; padding: 0.5rem; margin-top: 0.25rem; border: 1px solid #b9ae96; border-radius: 4px; box-sizing: border-box; font-family: inherit; font-size: 0.875rem; }}
                textarea {{ resize: vertical; min-height: 80px; }}
                .btn-submit {{ background: #24332d; color: #ffffff; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; font-weight: 600; margin-top: 1.5rem; cursor: pointer; width: 100%; font-size: 1rem; }}
                .btn-submit:hover {{ background: #ad793b; }}
                .btn-cancel {{ display: inline-block; text-align: center; color: #657067; margin-top: 0.75rem; width: 100%; text-decoration: none; font-size: 0.875rem; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>✨ Review & Create Venue</h1>
                <p style="color: #657067; font-size: 0.875rem; margin-bottom: 1rem;">Metadata extracted from Google Maps. Review and customize fields before publishing to production.</p>
                {alert_html}
                <form method="POST" action="/admin/add-venue-url">
                    <input type="hidden" name="action" value="save" />
                    <input type="hidden" name="google_maps_url" value="{parsed_data.get('url', '')}" />

                    <div class="grid">
                        <div>
                            <label for="name">Venue Name</label>
                            <input type="text" id="name" name="name" value="{parsed_data.get('name', '')}" required />
                        </div>
                        <div>
                            <label for="slug">Slug</label>
                            <input type="text" id="slug" name="slug" value="{parsed_data.get('slug', '')}" required />
                        </div>
                    </div>

                    <label for="address">Address</label>
                    <input type="text" id="address" name="address" value="{parsed_data.get('address', '')}" required />

                    <div class="grid">
                        <div>
                            <label for="latitude">Latitude</label>
                            <input type="number" step="any" id="latitude" name="latitude" value="{parsed_data.get('latitude', 30.0444)}" required />
                        </div>
                        <div>
                            <label for="longitude">Longitude</label>
                            <input type="number" step="any" id="longitude" name="longitude" value="{parsed_data.get('longitude', 31.2357)}" required />
                        </div>
                    </div>

                    <div class="grid">
                        <div>
                            <label for="category_id">Category</label>
                            <select id="category_id" name="category_id" required>
                                {cat_options}
                            </select>
                        </div>
                        <div>
                            <label for="price_range">Price Range</label>
                            <select id="price_range" name="price_range">
                                <option value="$" {"selected" if parsed_data.get("price_range") == "$" else ""}>$ (Budget)</option>
                                <option value="$$" {"selected" if parsed_data.get("price_range") == "$$" or not parsed_data.get("price_range") else ""}>$$ (Moderate)</option>
                                <option value="$$$" {"selected" if parsed_data.get("price_range") == "$$$" else ""}>$$$ (Upscale)</option>
                                <option value="$$$$" {"selected" if parsed_data.get("price_range") == "$$$$" else ""}>$$$$ (Luxury)</option>
                            </select>
                        </div>
                    </div>

                    <div class="grid">
                        <div>
                            <label for="working_hours">Working Hours</label>
                            <input type="text" id="working_hours" name="working_hours" value="{parsed_data.get('working_hours', '') or ''}" />
                        </div>
                        <div>
                            <label for="vibe_description">Short Vibe Description</label>
                            <input type="text" id="vibe_description" name="vibe_description" placeholder="e.g. Classic vintage pub vibe" />
                        </div>
                    </div>

                    <label for="photo_url">Main Photo URL</label>
                    <input type="url" id="photo_url" name="photo_url" value="{parsed_data.get('photo_url', '') or ''}" />

                    <label for="description">Detailed Description</label>
                    <textarea id="description" name="description" placeholder="Add detailed venue context or story..."></textarea>

                    <label>Vibe Tags</label>
                    <div style="background: #f9f7f1; padding: 0.75rem; border: 1px solid #b9ae96; border-radius: 4px; margin-top: 0.25rem;">
                        {vibe_checkboxes if vibe_checkboxes else '<span style="color:#657067; font-size:0.875rem;">No vibe tags available in database.</span>'}
                    </div>

                    <button type="submit" class="btn-submit">Publish Venue</button>
                    <a href="/admin/add-venue-url" class="btn-cancel">Cancel / Try another link</a>
                </form>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(html_content)



