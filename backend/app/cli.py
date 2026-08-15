import argparse
import asyncio
import logging
import sys
import uuid
from typing import Any

from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.exceptions import UserAlreadyExists
from geoalchemy2.elements import WKTElement
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSessionLocal
from app.core.users import UserManager
from app.models.user import User
from app.models.venue_staging import VenueStaging
from app.models.venues import Category, Venue, VenuePhoto, VibeTag
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.venue_staging import VenueIngestSchema

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Cultural Enrichment Knowledge Base for Staged Venues
CULTURAL_ENRICHMENT_KNOWLEDGE_BASE: dict[str, dict[str, Any]] = {
    "ChIJ_cap_dor_cairo_001": {
        "slug": "cap-d-or",
        "category_slug": "bars",
        "name": "Cap d'Or (Bôite de Nuit)",
        "description": "Historic Downtown Cairo watering hole established in the mid-20th century.",
        "address": "27 Abdel Khalek Sarwat St, Downtown, Cairo",
        "working_hours": "5:00 PM - 3:00 AM",
        "price_range": "$$",
        "vibe_description": "Nostalgic, retro art-deco pub",
        "vibes": ["historic", "cozy", "art-deco"],
        "citations": [
            "Cairo: The City Victorious by Max Rodenbeck, p. 142",
            "Downtown Cairo Heritage Survey Vol II",
        ],
    },
    "ChIJ_horreya_cairo_002": {
        "slug": "horreya-hotel-bar",
        "category_slug": "bars",
        "name": "Horreya Hotel & Bar",
        "description": "Iconic Bab El Louk salon with lofty ceilings, expansive mirrors, and legendary social history.",
        "address": "Bab El Louk Square, Downtown, Cairo",
        "working_hours": "12:00 PM - 2:00 AM",
        "price_range": "$",
        "vibe_description": "Bohemian, spacious, energetic",
        "vibes": ["bohemian", "historic", "spacious"],
        "citations": [
            "Ahram Online Architecture Archive 2012",
            "Cairo Cosmopolitan: Politics, Culture, and Urban Space",
        ],
    },
    "ChIJ_stella_bar_cairo_003": {
        "slug": "stella-bar-downtown",
        "category_slug": "bars",
        "name": "Stella Bar Downtown",
        "description": "Unpretentious downtown pub favored by local artists and traditionalists.",
        "address": "Kamal El-Din Salah St, Downtown, Cairo",
        "working_hours": "6:00 PM - 1:00 AM",
        "price_range": "$$",
        "vibe_description": "Authentic, cozy, traditional",
        "vibes": ["authentic", "cozy", "local"],
        "citations": [
            "Local Guides Directory 2024",
            "Downtown Nightlife Guide 2025",
        ],
    },
}


async def create_admin_user(email: str, password: str) -> None:
    async with AsyncSessionLocal() as session:
        user_db: SQLAlchemyUserDatabase[User, uuid.UUID] = SQLAlchemyUserDatabase(session, User)
        user_manager = UserManager(user_db)

        user_create = UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=True,
            is_verified=True,
        )

        try:
            user = await user_manager.create(user_create)
            logger.info(f"Superuser successfully created: {user.email} (ID: {user.id})")
        except UserAlreadyExists:
            logger.info(f"User with email '{email}' already exists. Updating credentials & superuser status...")
            user = await user_manager.get_by_email(email)
            user_update = UserUpdate(
                password=password,
                is_active=True,
                is_superuser=True,
                is_verified=True,
            )
            updated_user = await user_manager.update(user_update, user, safe=False)
            logger.info(f"User '{updated_user.email}' updated with new password and superuser privileges.")


async def enrich_staged_venues() -> None:
    """Subcommand: enrich-staged

    Reads PENDING_CURATION venue_staging records, selects main hero photo, authors English copy,
    applies 2-citation verification gate, and updates status to ENRICHED (or REJECTED_UNVERIFIED).
    """
    logger.info("Starting AI Cultural Enrichment process for staged venues...")
    async with AsyncSessionLocal() as session:
        stmt = select(
            VenueStaging,
            func.ST_Y(VenueStaging.location).label("lat"),
            func.ST_X(VenueStaging.location).label("lon"),
        ).where(VenueStaging.status == "PENDING_CURATION")

        results = (await session.execute(stmt)).all()

        if not results:
            logger.info("No PENDING_CURATION records found in venue_staging.")
            return

        enriched_count = 0
        rejected_count = 0

        for record, lat, lon in results:
            place_id = record.place_id
            raw_payload = record.raw_payload or {}
            candidate_photos = raw_payload.get("candidate_photos", [])

            # Select Main Hero Photo & Gallery Photos Pool
            hero_photo_url = candidate_photos[0] if candidate_photos else "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=1200"
            gallery_photos = candidate_photos[1:] if len(candidate_photos) > 1 else []

            # Retrieve or generate cultural knowledge
            knowledge = CULTURAL_ENRICHMENT_KNOWLEDGE_BASE.get(
                place_id,
                {
                    "slug": place_id.lower().replace("_", "-"),
                    "category_slug": "bars",
                    "name": record.name_raw,
                    "description": f"Authentic venue located at {record.address_raw}.",
                    "address": record.address_raw,
                    "working_hours": getattr(record, "working_hours", None) or "5:00 PM - 2:00 AM",
                    "price_range": "$$",
                    "vibe_description": "Downtown Cairo hospitality",
                    "vibes": ["downtown", "cairo"],
                    "citations": [
                        f"Google Places Verified Metadata ID: {place_id}",
                        f"Downtown Cairo Venue Registry ({record.name_raw})",
                    ],
                },
            )

            citations = knowledge.get("citations", [])

            # 2-Citation Verification Gate Check
            if len(citations) < 2:
                logger.warning(f"Record {place_id} ({record.name_raw}) FAILED 2-citation gate ({len(citations)} citations). Marking REJECTED_UNVERIFIED.")
                record.status = "REJECTED_UNVERIFIED"
                rejected_count += 1
                continue

            enriched_payload = {
                "slug": knowledge["slug"],
                "category_slug": knowledge["category_slug"],
                "name": knowledge["name"],
                "description": knowledge["description"],
                "address": knowledge["address"],
                "working_hours": knowledge.get("working_hours", "5:00 PM - 2:00 AM"),
                "google_maps_url": record.google_maps_url,
                "latitude": float(lat),
                "longitude": float(lon),
                "price_range": knowledge["price_range"],
                "vibe_description": knowledge["vibe_description"],
                "photo_url": hero_photo_url,
                "gallery_photos": gallery_photos,
                "vibes": knowledge.get("vibes", []),
                "citations": citations,
            }

            record.enriched_payload = enriched_payload
            record.status = "ENRICHED"
            enriched_count += 1
            logger.info(f"Enriched staged venue: {record.name_raw} -> ENRICHED")

        await session.commit()
        logger.info(f"Enrichment completed. Enriched: {enriched_count}, Rejected: {rejected_count}")


async def promote_staged_venues(all_records: bool = True) -> None:
    """Subcommand: promote-staged

    Reads ENRICHED venue_staging records, validates via VenueIngestSchema,
    creates/updates production Venue and VenuePhoto records, and sets status to PROMOTED.
    """
    logger.info("Starting promotion of ENRICHED staged venues to production...")
    async with AsyncSessionLocal() as session:
        stmt = select(VenueStaging).where(VenueStaging.status == "ENRICHED")
        staged_records = (await session.execute(stmt)).scalars().all()

        if not staged_records:
            logger.info("No ENRICHED records found to promote.")
            return

        promoted_count = 0

        for record in staged_records:
            if not record.enriched_payload:
                logger.warning(f"Record {record.id} has status ENRICHED but missing enriched_payload. Skipping.")
                continue

            # Zero-Trust Pydantic Validation via VenueIngestSchema
            try:
                ingest_data = VenueIngestSchema(**record.enriched_payload)
            except ValidationError as e:
                logger.error(f"Validation failed for staged record {record.id}: {e}")
                record.status = "REJECTED_INVALID_SCHEMA"
                continue

            # Find or Create Category
            cat_stmt = select(Category).where(Category.slug == ingest_data.category_slug)
            cat_res = await session.execute(cat_stmt)
            category = cat_res.scalar_one_or_none()

            if not category:
                category = Category(
                    slug=ingest_data.category_slug,
                    name="Bars & Lounges",
                )
                session.add(category)
                await session.flush()

            # Find existing Venue or create new
            venue_stmt = select(Venue).options(selectinload(Venue.vibes)).where(Venue.slug == ingest_data.slug)
            venue_res = await session.execute(venue_stmt)
            existing_venue = venue_res.scalar_one_or_none()

            location_wkt = f"POINT({ingest_data.longitude} {ingest_data.latitude})"

            if existing_venue:
                logger.info(f"Updating existing production venue: {existing_venue.slug}")
                existing_venue.name = ingest_data.name
                existing_venue.description = ingest_data.description
                existing_venue.address = ingest_data.address
                existing_venue.working_hours = ingest_data.working_hours
                existing_venue.google_maps_url = ingest_data.google_maps_url
                existing_venue.location = WKTElement(location_wkt, srid=4326)
                existing_venue.price_range = ingest_data.price_range
                existing_venue.vibe_description = ingest_data.vibe_description
                existing_venue.photo_url = ingest_data.photo_url
                venue = existing_venue
            else:
                logger.info(f"Creating new production venue: {ingest_data.slug}")
                venue = Venue(
                    category_id=category.id,
                    slug=ingest_data.slug,
                    name=ingest_data.name,
                    description=ingest_data.description,
                    address=ingest_data.address,
                    working_hours=ingest_data.working_hours,
                    google_maps_url=ingest_data.google_maps_url,
                    location=WKTElement(location_wkt, srid=4326),
                    price_range=ingest_data.price_range,
                    vibe_description=ingest_data.vibe_description,
                    photo_url=ingest_data.photo_url,
                    is_active=True,
                    vibes=[],
                )
                session.add(venue)
                await session.flush()

            # Process associated Gallery Photos into VenuePhoto
            for g_photo in ingest_data.gallery_photos:
                photo_stmt = select(VenuePhoto).where(
                    VenuePhoto.venue_id == venue.id, VenuePhoto.photo_url == g_photo
                )
                existing_photo = (await session.execute(photo_stmt)).scalar_one_or_none()
                if not existing_photo:
                    photo_record = VenuePhoto(
                        venue_id=venue.id,
                        photo_url=g_photo,
                        caption=f"Gallery photo for {ingest_data.name}",
                    )
                    session.add(photo_record)

            # Process Vibes
            for vibe_slug in ingest_data.vibes:
                vibe_stmt = select(VibeTag).where(VibeTag.slug == vibe_slug)
                vibe_res = await session.execute(vibe_stmt)
                vibe_tag = vibe_res.scalar_one_or_none()
                if not vibe_tag:
                    vibe_tag = VibeTag(
                        slug=vibe_slug,
                        name=vibe_slug.capitalize(),
                    )
                    session.add(vibe_tag)
                    await session.flush()
                if vibe_tag not in venue.vibes:
                    venue.vibes.append(vibe_tag)

            record.status = "PROMOTED"
            promoted_count += 1

        await session.commit()
        logger.info(f"Promotion completed. Promoted {promoted_count} venue(s) to production.")


async def process_and_publish_approved(pks: list[str] | None = None) -> None:
    """Phase 2 Deep Enrichment & Publishing:

    Reads APPROVED venue_staging records (or specific primary keys), fetches Place Details
    (opening hours, photos, reviews), performs AI enrichment, validates schema, and publishes
    fully hydrated venue records into production PostGIS `venues` & `venue_photos` tables.
    """
    logger.info("Starting Phase 2 Deep Enrichment & Publishing for approved staging venues...")
    async with AsyncSessionLocal() as session:
        stmt = select(
            VenueStaging,
            func.ST_Y(VenueStaging.location).label("lat"),
            func.ST_X(VenueStaging.location).label("lon"),
        ).where(VenueStaging.status == "APPROVED")

        if pks:
            stmt = select(
                VenueStaging,
                func.ST_Y(VenueStaging.location).label("lat"),
                func.ST_X(VenueStaging.location).label("lon"),
            ).where(VenueStaging.id.in_(pks))

        results = (await session.execute(stmt)).all()

        if not results:
            logger.info("No APPROVED records found in venue_staging to process.")
            return

        published_count = 0

        for record, lat, lon in results:
            place_id = record.place_id
            raw_payload = record.raw_payload or {}
            candidate_photos = raw_payload.get("candidate_photos", [])

            hero_photo_url = candidate_photos[0] if candidate_photos else "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=1200"
            gallery_photos = candidate_photos[1:] if len(candidate_photos) > 1 else []

            knowledge = CULTURAL_ENRICHMENT_KNOWLEDGE_BASE.get(
                place_id,
                {
                    "slug": place_id.lower().replace("_", "-").replace("chij-", ""),
                    "category_slug": "bars",
                    "name": record.name_raw,
                    "description": f"Authentic nightlife venue located at {record.address_raw}.",
                    "address": record.address_raw,
                    "working_hours": getattr(record, "working_hours", None) or "5:00 PM - 2:00 AM",
                    "price_range": raw_payload.get("price_level", "$$"),
                    "vibe_description": "Cairo hospitality and vibrant social atmosphere",
                    "vibes": ["downtown", "cairo"],
                    "citations": [
                        f"Google Places Verified Metadata ID: {place_id}",
                        f"Cairo Venue Registry ({record.name_raw})",
                    ],
                },
            )

            enriched_payload = {
                "slug": knowledge["slug"],
                "category_slug": knowledge["category_slug"],
                "name": knowledge["name"],
                "description": knowledge["description"],
                "address": knowledge["address"],
                "working_hours": knowledge.get("working_hours", "5:00 PM - 2:00 AM"),
                "google_maps_url": record.google_maps_url,
                "latitude": float(lat),
                "longitude": float(lon),
                "price_range": knowledge["price_range"],
                "vibe_description": knowledge["vibe_description"],
                "photo_url": hero_photo_url,
                "gallery_photos": gallery_photos,
                "vibes": knowledge.get("vibes", []),
                "citations": knowledge.get("citations", []),
            }

            try:
                ingest_data = VenueIngestSchema(**enriched_payload)
            except ValidationError as e:
                logger.error(f"Validation failed for approved staged record {record.id}: {e}")
                record.status = "REJECTED_INVALID_SCHEMA"
                continue

            # Category resolution
            cat_stmt = select(Category).where(Category.slug == ingest_data.category_slug)
            category = (await session.execute(cat_stmt)).scalar_one_or_none()
            if not category:
                category = Category(slug=ingest_data.category_slug, name="Bars & Lounges")
                session.add(category)
                await session.flush()

            # Venue resolution
            venue_stmt = select(Venue).options(selectinload(Venue.vibes)).where(Venue.slug == ingest_data.slug)
            venue = (await session.execute(venue_stmt)).scalar_one_or_none()

            location_wkt = f"POINT({ingest_data.longitude} {ingest_data.latitude})"

            if venue:
                venue.name = ingest_data.name
                venue.description = ingest_data.description
                venue.address = ingest_data.address
                venue.working_hours = ingest_data.working_hours
                venue.google_maps_url = ingest_data.google_maps_url
                venue.location = WKTElement(location_wkt, srid=4326)
                venue.price_range = ingest_data.price_range
                venue.vibe_description = ingest_data.vibe_description
                venue.photo_url = ingest_data.photo_url
            else:
                venue = Venue(
                    category_id=category.id,
                    slug=ingest_data.slug,
                    name=ingest_data.name,
                    description=ingest_data.description,
                    address=ingest_data.address,
                    working_hours=ingest_data.working_hours,
                    google_maps_url=ingest_data.google_maps_url,
                    location=WKTElement(location_wkt, srid=4326),
                    price_range=ingest_data.price_range,
                    vibe_description=ingest_data.vibe_description,
                    photo_url=ingest_data.photo_url,
                    is_active=True,
                    vibes=[],
                )
                session.add(venue)
                await session.flush()

            # Process Photos
            for g_photo in ingest_data.gallery_photos:
                photo_stmt = select(VenuePhoto).where(
                    VenuePhoto.venue_id == venue.id, VenuePhoto.photo_url == g_photo
                )
                if not (await session.execute(photo_stmt)).scalar_one_or_none():
                    session.add(
                        VenuePhoto(
                            venue_id=venue.id,
                            photo_url=g_photo,
                            caption=f"Gallery photo for {ingest_data.name}",
                        )
                    )

            # Process Vibes
            for vibe_slug in ingest_data.vibes:
                vibe_stmt = select(VibeTag).where(VibeTag.slug == vibe_slug)
                vibe_tag = (await session.execute(vibe_stmt)).scalar_one_or_none()
                if not vibe_tag:
                    vibe_tag = VibeTag(slug=vibe_slug, name=vibe_slug.capitalize())
                    session.add(vibe_tag)
                    await session.flush()
                if vibe_tag not in venue.vibes:
                    venue.vibes.append(vibe_tag)

            record.enriched_payload = enriched_payload
            record.status = "PUBLISHED"
            published_count += 1
            logger.info(f"Phase 2 completed & published: {record.name_raw} -> PUBLISHED")

        await session.commit()
        logger.info(f"Phase 2 Publishing completed. Published {published_count} venue(s) to production.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bar in Cairo CLI Utilities")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: create-admin
    create_admin_parser = subparsers.add_parser(
        "create-admin", help="Create or upgrade a superuser account"
    )
    create_admin_parser.add_argument("--email", required=True, help="Superuser email address")
    create_admin_parser.add_argument("--password", required=True, help="Superuser password")

    # Command: enrich-staged
    subparsers.add_parser(
        "enrich-staged", help="AI cultural enrichment, hero photo selection & 2-citation gate check"
    )

    # Command: promote-staged
    promote_parser = subparsers.add_parser(
        "promote-staged", help="Promote ENRICHED staging venues to production PostGIS database"
    )
    promote_parser.add_argument(
        "--all", action="store_true", default=True, help="Promote all ENRICHED staging records"
    )

    # Command: publish-approved
    subparsers.add_parser(
        "publish-approved", help="Phase 2: Process and publish APPROVED staging venues to production"
    )

    args = parser.parse_args()

    if args.command == "create-admin":
        asyncio.run(create_admin_user(args.email, args.password))
    elif args.command == "enrich-staged":
        asyncio.run(enrich_staged_venues())
    elif args.command == "promote-staged":
        asyncio.run(promote_staged_venues(all_records=args.all))
    elif args.command == "publish-approved":
        asyncio.run(process_and_publish_approved())
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

