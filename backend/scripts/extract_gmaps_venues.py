import argparse
import asyncio
import logging
import os
import sys
from typing import Any

import httpx
from dotenv import load_dotenv
from geoalchemy2.elements import WKTElement
from sqlalchemy import func, select

from app.core.database import AsyncSessionLocal
from app.models.venue_staging import VenueStaging
from app.models.venues import Venue

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def is_within_bbox(lat: float, lon: float, bbox: tuple[float, float, float, float]) -> bool:
    """Check if lat/lon is strictly within bounding box (lat_min, lon_min, lat_max, lon_max)."""
    lat_min, lon_min, lat_max, lon_max = bbox
    return lat_min <= lat <= lat_max and lon_min <= lon <= lon_max


def parse_bbox(bbox_str: str) -> tuple[float, float, float, float]:
    """Parse comma-separated bbox string into 4 floats."""
    parts = [float(p.strip()) for p in bbox_str.split(",")]
    if len(parts) != 4:
        raise ValueError("BBox must contain 4 comma-separated floats: lat_min,lon_min,lat_max,lon_max")
    return parts[0], parts[1], parts[2], parts[3]


def synthesize_what_people_say(reviews: list[str]) -> str:
    """Synthesize a clean review summary block 'what_people_say' from extracted review snippets."""
    if not reviews:
        return "Popular venue with authentic local character."
    summary_bullets = " | ".join(r.strip().rstrip(".") for r in reviews[:3])
    return f"Visitors highlight: {summary_bullets}."


async def fetch_places_from_google_api(location: str, qty: int) -> list[dict[str, Any]]:
    """Phase 1: Fetch lightweight search results via Google Places API with explicit error handling."""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_MAPS_API_KEY is not configured in .env. A valid Google Maps API Key is required for live extraction."
        )

    query_text = f"bars in {location}" if "bar" not in location.lower() else location
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    items: list[dict[str, Any]] = []
    async with httpx.AsyncClient(timeout=25.0) as client:
        params = {"query": query_text, "key": api_key}
        logger.info(f"Querying Google Places Text Search API for '{query_text}'...")
        response = await client.get(url, params=params)
        data = response.json()

        api_status = data.get("status")
        if api_status == "REQUEST_DENIED":
            error_msg = data.get(
                "error_message",
                "Request denied by Google Maps Platform. Ensure billing is enabled on your Google Cloud Project.",
            )
            logger.error(f"Google Places API Error (REQUEST_DENIED): {error_msg}")
            raise ValueError(f"Google Places API Error (REQUEST_DENIED): {error_msg}")
        elif api_status not in ("OK", "ZERO_RESULTS"):
            error_msg = data.get("error_message", f"API returned status {api_status}")
            logger.error(f"Google Places API Error ({api_status}): {error_msg}")
            raise ValueError(f"Google Places API Error ({api_status}): {error_msg}")

        results = data.get("results", [])
        logger.info(f"Google Places API returned {len(results)} search results for '{query_text}'.")
        for place in results:
            place_id = place.get("place_id")
            if not place_id:
                continue

            lat = place.get("geometry", {}).get("location", {}).get("lat")
            lng = place.get("geometry", {}).get("location", {}).get("lng")
            if lat is None or lng is None:
                continue

            types = place.get("types", [])
            primary_type = types[0] if types else "bar"

            items.append(
                {
                    "place_id": place_id,
                    "name_raw": place.get("name", "Unknown Venue"),
                    "address_raw": place.get("formatted_address", f"{location}, Cairo"),
                    "latitude": float(lat),
                    "longitude": float(lng),
                    "google_maps_url": f"https://www.google.com/maps/place/?q=place_id:{place_id}",
                    "price_level": "$" * (place.get("price_level", 2) or 2),
                    "rating": place.get("rating"),
                    "user_ratings_total": place.get("user_ratings_total"),
                    "primary_type": primary_type,
                    "business_status": place.get("business_status", "OPERATIONAL"),
                }
            )

    return items[:qty]


async def extract_and_stage_venues(
    location: str = "downtown",
    qty: int = 10,
    dry_run: bool = False,
    bbox: tuple[float, float, float, float] | None = None,
    fixtures_only: bool = True,
) -> list[dict[str, Any]]:
    """Phase 1 Extraction: Fetch lightweight search results and stage un-duplicated entries as PENDING_CURATION."""
    logger.info(f"Phase 1 Extraction started for location='{location}', requested max qty={qty}")

    raw_items = await fetch_places_from_google_api(location=location, qty=qty * 2)

    processed_records: list[dict[str, Any]] = []

    async with AsyncSessionLocal() as session:
        for item in raw_items:
            if len(processed_records) >= qty:
                logger.info(f"Reached requested limit of {qty} new un-staged venue(s).")
                break

            place_id = item["place_id"]
            lat = item["latitude"]
            lon = item["longitude"]

            if bbox and not is_within_bbox(lat, lon, bbox):
                logger.warning(f"Skipping {item['name_raw']} - outside bbox constraints ({lat}, {lon})")
                continue

            # Deduplication Check 1: place_id in venue_staging
            stmt_staging = select(VenueStaging).where(VenueStaging.place_id == place_id)
            res_staging = await session.execute(stmt_staging)
            if res_staging.scalar_one_or_none():
                logger.info(f"Deduplication hit (place_id in staging): {place_id} ({item['name_raw']})")
                continue

            # Deduplication Check 2: place_id / spatial proximity in production venues
            point_geom = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
            stmt_spatial_staging = select(VenueStaging).where(
                func.ST_DWithin(
                    func.ST_Transform(VenueStaging.location, 3857),
                    func.ST_Transform(point_geom, 3857),
                    15.0,  # 15 meters radius check
                )
            )
            res_spatial_staging = await session.execute(stmt_spatial_staging)
            if res_spatial_staging.scalar_one_or_none():
                logger.info(f"Deduplication hit (spatial proximity <15m in staging): {item['name_raw']}")
                continue

            stmt_spatial_prod = select(Venue).where(
                func.ST_DWithin(
                    func.ST_Transform(Venue.location, 3857),
                    func.ST_Transform(point_geom, 3857),
                    15.0,
                )
            )
            res_spatial_prod = await session.execute(stmt_spatial_prod)
            if res_spatial_prod.scalar_one_or_none():
                logger.info(f"Deduplication hit (spatial proximity <15m in production): {item['name_raw']}")
                continue

            raw_payload = {
                "place_id": place_id,
                "price_level": item.get("price_level", "$$"),
                "rating": item.get("rating"),
                "user_ratings_total": item.get("user_ratings_total"),
                "primary_type": item.get("primary_type", "bar"),
                "business_status": item.get("business_status", "OPERATIONAL"),
                "extracted_via": "extract_gmaps_venues.py (Phase 1)",
            }

            location_wkt = f"POINT({lon} {lat})"

            staging_record = {
                "place_id": place_id,
                "google_maps_url": item["google_maps_url"],
                "name_raw": item["name_raw"],
                "address_raw": item["address_raw"],
                "location": location_wkt,
                "raw_payload": raw_payload,
                "status": "PENDING_CURATION",
            }

            processed_records.append(staging_record)

            if not dry_run:
                db_record = VenueStaging(
                    place_id=place_id,
                    google_maps_url=item["google_maps_url"],
                    name_raw=item["name_raw"],
                    address_raw=item["address_raw"],
                    location=WKTElement(location_wkt, srid=4326),
                    raw_payload=raw_payload,
                    status="PENDING_CURATION",
                )
                session.add(db_record)

        if not dry_run and processed_records:
            await session.commit()
            logger.info(f"Successfully staged {len(processed_records)} new venue records into venue_staging.")
        elif dry_run:
            logger.info(f"[DRY-RUN] Would stage {len(processed_records)} new records into venue_staging.")

    return processed_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 1: Lightweight Google Places Search & Staging")
    parser.add_argument(
        "--in",
        "--location",
        dest="location",
        type=str,
        default="downtown",
        help="Target location or district (e.g. heliopolis, downtown, maadi, zamalek)",
    )
    parser.add_argument(
        "--qty",
        "--max-count",
        dest="qty",
        type=int,
        default=10,
        help="Maximum quantity of new un-staged venues to extract into venue_staging",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Execute extraction without writing records to database",
    )

    args = parser.parse_args()
    try:
        records = asyncio.run(extract_and_stage_venues(location=args.location, qty=args.qty, dry_run=args.dry_run))
        print(f"Extraction summary: {len(records)} record(s) staged.")
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
