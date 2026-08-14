import argparse
import asyncio
import logging
import os
import sys
from typing import Any

from geoalchemy2.elements import WKTElement
from sqlalchemy import func, select

from app.core.database import AsyncSessionLocal
from app.models.venue_staging import VenueStaging
from app.models.venues import Venue

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Sample Downtown Cairo Venue Fixtures for Extraction & Verification
DOWNTOWN_FIXTURES: list[dict[str, Any]] = [
    {
        "place_id": "ChIJ_cap_dor_cairo_001",
        "name_raw": "Cap d'Or (Bôite de Nuit)",
        "address_raw": "27 Abdel Khalek Sarwat St, Downtown, Cairo, Egypt",
        "latitude": 30.0452,
        "longitude": 31.2385,
        "google_maps_url": "https://www.google.com/maps/place/?q=place_id:ChIJ_cap_dor_cairo_001",
        "candidate_photos": [
            "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=1200&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1572116469696-31de0f17cc34?w=1200&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1543007630-9710e4a00a20?w=1200&auto=format&fit=crop",
        ],
        "reviews": [
            "Classic Downtown Cairo art-deco watering hole. Legendary wooden bar and retro ambiance.",
            "Historical bar frequented by artists, journalists, and intellectuals since the 1940s.",
            "Cold Stella beer, excellent lupin beans (termis), and friendly nostalgic atmosphere.",
        ],
    },
    {
        "place_id": "ChIJ_horreya_cairo_002",
        "name_raw": "Horreya Hotel & Bar",
        "address_raw": "Bab El Louk Square, Downtown, Cairo, Egypt",
        "latitude": 30.0428,
        "longitude": 31.2392,
        "google_maps_url": "https://www.google.com/maps/place/?q=place_id:ChIJ_horreya_cairo_002",
        "candidate_photos": [
            "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=1200&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1574096079513-d8259312b785?w=1200&auto=format&fit=crop",
        ],
        "reviews": [
            "High ceilings, open mirrors, and vibrant cosmopolitan crowds in Bab El Louk.",
            "An iconic meeting hub for Cairo creatives, students, and travelers.",
            "Generous space, cold local brews, and bustling downtown energy.",
        ],
    },
    {
        "place_id": "ChIJ_stella_bar_cairo_003",
        "name_raw": "Stella Bar Downtown",
        "address_raw": "Kamal El-Din Salah St, Downtown, Cairo, Egypt",
        "latitude": 30.0441,
        "longitude": 31.2355,
        "google_maps_url": "https://www.google.com/maps/place/?q=place_id:ChIJ_stella_bar_cairo_003",
        "candidate_photos": [
            "https://images.unsplash.com/photo-1538488881525-4a69676e1a4f?w=1200&auto=format&fit=crop",
        ],
        "reviews": [
            "Unpretentious local favorite for evening drinks and conversation.",
            "Cozy traditional downtown pub atmosphere with attentive service.",
        ],
    },
    {
        "place_id": "ChIJ_odeon_rooftop_cairo_004",
        "name_raw": "Odeon Palace Rooftop Bar",
        "address_raw": "6 Abdel Hamid Said St, Downtown, Cairo, Egypt",
        "latitude": 30.0485,
        "longitude": 31.2410,
        "google_maps_url": "https://www.google.com/maps/place/?q=place_id:ChIJ_odeon_rooftop_cairo_004",
        "candidate_photos": [
            "https://images.unsplash.com/photo-1572116469696-31de0f17cc34?w=1200&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=1200&auto=format&fit=crop",
        ],
        "reviews": [
            "24-hour rooftop terrace overlooking historic Downtown Cairo roofs.",
            "Relaxed open-air atmosphere with views of classic 1930s architecture.",
        ],
    },
    {
        "place_id": "ChIJ_windsor_barrel_cairo_005",
        "name_raw": "Windsor Barrel Bar",
        "address_raw": "19 Al Alfi St, Downtown, Cairo, Egypt",
        "latitude": 30.0515,
        "longitude": 31.2462,
        "google_maps_url": "https://www.google.com/maps/place/?q=place_id:ChIJ_windsor_barrel_cairo_005",
        "candidate_photos": [
            "https://images.unsplash.com/photo-1543007630-9710e4a00a20?w=1200&auto=format&fit=crop",
        ],
        "reviews": [
            "Historic hotel bar with original wooden barrels and colonial memorabilia.",
            "Charming time capsule in the heart of Downtown Cairo.",
        ],
    },
]


def synthesize_what_people_say(reviews: list[str]) -> str:
    """Synthesize a clean review summary block 'what_people_say' from extracted review snippets."""
    if not reviews:
        return "Popular downtown Cairo venue with authentic local character."
    summary_bullets = " | ".join(r.strip().rstrip(".") for r in reviews[:3])
    return f"Visitors highlight: {summary_bullets}."


def is_within_bbox(lat: float, lon: float, bbox: tuple[float, float, float, float]) -> bool:
    """Check if lat/lon is strictly within bounding box (lat_min, lon_min, lat_max, lon_max)."""
    lat_min, lon_min, lat_max, lon_max = bbox
    return lat_min <= lat <= lat_max and lon_min <= lon <= lon_max


async def extract_and_stage_venues(
    bbox: tuple[float, float, float, float],
    dry_run: bool = False,
    fixtures_only: bool = True,
) -> list[dict[str, Any]]:
    lat_min, lon_min, lat_max, lon_max = bbox
    logger.info(f"Starting extraction for bounding box: N{lat_min}-{lat_max}°, E{lon_min}-{lon_max}°")

    raw_items = DOWNTOWN_FIXTURES if fixtures_only or not os.getenv("GOOGLE_MAPS_API_KEY") else []

    processed_records: list[dict[str, Any]] = []

    async with AsyncSessionLocal() as session:
        for item in raw_items:
            lat = item["latitude"]
            lon = item["longitude"]

            if not is_within_bbox(lat, lon, bbox):
                logger.warning(f"Skipping {item['name_raw']} - outside bbox constraints ({lat}, {lon})")
                continue

            place_id = item["place_id"]
            # Deduplication Check 1: Existing place_id in venue_staging
            stmt_staging = select(VenueStaging).where(VenueStaging.place_id == place_id)
            res_staging = await session.execute(stmt_staging)
            existing_staged = res_staging.scalar_one_or_none()

            if existing_staged:
                logger.info(f"Deduplication hit (place_id in staging): {place_id} ({item['name_raw']})")
                continue

            # Deduplication Check 2: PostGIS ST_DWithin spatial proximity check (15 meters)
            point_geom = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
            stmt_spatial = select(VenueStaging).where(
                func.ST_DWithin(
                    func.ST_Transform(VenueStaging.location, 3857),
                    func.ST_Transform(point_geom, 3857),
                    15.0,  # 15 meters
                )
            )
            res_spatial = await session.execute(stmt_spatial)
            nearby_staged = res_spatial.scalar_one_or_none()

            if nearby_staged:
                logger.info(
                    f"Deduplication hit (spatial proximity <15m in staging): {item['name_raw']} near {nearby_staged.name_raw}"
                )
                continue

            # Deduplication Check 3: Check production venues table by location
            stmt_prod = select(Venue).where(
                func.ST_DWithin(
                    func.ST_Transform(Venue.location, 3857),
                    func.ST_Transform(point_geom, 3857),
                    15.0,
                )
            )
            res_prod = await session.execute(stmt_prod)
            nearby_prod = res_prod.scalar_one_or_none()

            if nearby_prod:
                logger.info(f"Deduplication hit (spatial proximity <15m in production): {item['name_raw']} near {nearby_prod.name_en}")
                continue

            reviews = item.get("reviews", [])
            what_people_say = synthesize_what_people_say(reviews)

            raw_payload = {
                "place_id": place_id,
                "candidate_photos": item.get("candidate_photos", []),
                "reviews": reviews,
                "what_people_say": what_people_say,
                "extracted_via": "extract_gmaps_venues.py",
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


def parse_bbox(bbox_str: str) -> tuple[float, float, float, float]:
    parts = [float(p.strip()) for p in bbox_str.split(",")]
    if len(parts) != 4:
        raise ValueError("BBox must contain 4 comma-separated floats: lat_min,lon_min,lat_max,lon_max")
    return parts[0], parts[1], parts[2], parts[3]


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 1: Deterministic Google Maps Venue & Reviews Extraction")
    parser.add_argument(
        "--bbox",
        type=str,
        default="30.0380,31.2300,30.0520,31.2480",
        help="Downtown Cairo bounding box: lat_min,lon_min,lat_max,lon_max",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Execute extraction without writing records to database",
    )
    parser.add_argument(
        "--fixtures",
        action="store_true",
        default=True,
        help="Use sample Downtown Cairo place fixtures",
    )

    args = parser.parse_args()

    try:
        bbox = parse_bbox(args.bbox)
    except ValueError as e:
        logger.error(f"Invalid --bbox format: {e}")
        sys.exit(1)

    records = asyncio.run(extract_and_stage_venues(bbox=bbox, dry_run=args.dry_run, fixtures_only=args.fixtures))
    print(f"Extraction summary: {len(records)} record(s) processed.")


if __name__ == "__main__":
    main()
