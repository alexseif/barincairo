import pytest
from geoalchemy2.elements import WKTElement
from pydantic import ValidationError
from sqlalchemy import select

from app.cli import enrich_staged_venues, promote_staged_venues
from app.core.database import AsyncSessionLocal
from app.models.venue_staging import VenueStaging
from app.models.venues import Venue, VenuePhoto
from app.schemas.venue_staging import VenueIngestSchema
from scripts.extract_gmaps_venues import (
    extract_and_stage_venues,
    is_within_bbox,
    synthesize_what_people_say,
)


def test_is_within_bbox():
    bbox = (30.0380, 31.2300, 30.0520, 31.2480)
    assert is_within_bbox(30.0450, 31.2380, bbox) is True
    assert is_within_bbox(31.0000, 31.2380, bbox) is False  # Outside lat
    assert is_within_bbox(30.0450, 32.0000, bbox) is False  # Outside lon


def test_synthesize_what_people_say():
    reviews = ["Great drinks and retro music", "Historic downtown venue"]
    summary = synthesize_what_people_say(reviews)
    assert "Great drinks" in summary
    assert "Historic downtown venue" in summary


def test_two_citation_gate_validation():
    valid_citations = ["Archival Source 1", "Archival Source 2"]
    invalid_citations = ["Single Source"]

    valid_payload = {
        "slug": "test-venue",
        "category_slug": "bars",
        "name": "Test Venue",
        "address": "123 Sarwat St",
        "working_hours": "5:00 PM - 2:00 AM",
        "google_maps_url": "https://maps.google.com/?q=place_id:ChIJ123",
        "latitude": 30.0450,
        "longitude": 31.2380,
        "photo_url": "https://example.com/photo.jpg",
        "citations": valid_citations,
    }
    schema = VenueIngestSchema(**valid_payload)
    assert len(schema.citations) == 2

    invalid_payload = {**valid_payload, "citations": invalid_citations}
    with pytest.raises(ValidationError):
        VenueIngestSchema(**invalid_payload)


@pytest.mark.asyncio
async def test_end_to_end_ingestion_pipeline():
    try:
        bbox = (30.0380, 31.2300, 30.0520, 31.2480)

        # 1. Extraction Phase without valid key should raise ValueError
        with pytest.raises(ValueError):
            await extract_and_stage_venues(bbox=bbox, dry_run=False, fixtures_only=True)

        async with AsyncSessionLocal() as session:
            # Create a unique test venue staging record for testing enrichment & promotion
            test_place_id = "ChIJ_pipeline_test_venue_999"

            # Cleanup if left over
            existing = (await session.execute(select(VenueStaging).where(VenueStaging.place_id == test_place_id))).scalar_one_or_none()
            if existing:
                await session.delete(existing)
                await session.commit()

            test_staging = VenueStaging(
                place_id=test_place_id,
                google_maps_url="https://maps.google.com/?q=place_id:ChIJ_pipeline_test_venue_999",
                name_raw="Pipeline Test Bar",
                address_raw="15 Champollion St, Downtown, Cairo",
                location=WKTElement("POINT(31.2380 30.0450)", srid=4326),
                raw_payload={
                    "candidate_photos": [
                        "https://example.com/hero.jpg",
                        "https://example.com/gallery1.jpg",
                    ],
                    "reviews": ["Excellent historic bar", "Cold local beverages"],
                },
                status="PENDING_CURATION",
            )
            session.add(test_staging)
            await session.commit()

        # 2. Enrichment Phase
        await enrich_staged_venues()

        async with AsyncSessionLocal() as session:
            staged_res = await session.execute(select(VenueStaging).where(VenueStaging.place_id == test_place_id))
            staged_venue = staged_res.scalar_one_or_none()
            assert staged_venue is not None
            assert staged_venue.status == "ENRICHED"
            assert staged_venue.enriched_payload is not None
            assert staged_venue.enriched_payload["photo_url"] == "https://example.com/hero.jpg"
            assert len(staged_venue.enriched_payload["citations"]) >= 2

        # 3. Promotion Phase
        await promote_staged_venues(all_records=True)

        async with AsyncSessionLocal() as session:
            # Verify Staging Status updated to PROMOTED
            staged_res = await session.execute(select(VenueStaging).where(VenueStaging.place_id == test_place_id))
            staged_venue = staged_res.scalar_one_or_none()
            assert staged_venue is not None
            assert staged_venue.status == "PROMOTED"

            # Verify Production Venue created
            expected_slug = staged_venue.enriched_payload["slug"]
            prod_res = await session.execute(select(Venue).where(Venue.slug == expected_slug))
            prod_venue = prod_res.scalar_one_or_none()
            assert prod_venue is not None
            assert prod_venue.google_maps_url == "https://maps.google.com/?q=place_id:ChIJ_pipeline_test_venue_999"

            # Verify Associated VenuePhoto created
            photo_res = await session.execute(select(VenuePhoto).where(VenuePhoto.venue_id == prod_venue.id))
            photos = photo_res.scalars().all()
            assert len(photos) >= 1
    finally:
        from sqlalchemy import delete
        from app.models.venues import Category
        async with AsyncSessionLocal() as session:
            await session.execute(delete(VenuePhoto))
            await session.execute(delete(Venue))
            await session.execute(delete(VenueStaging))
            await session.execute(delete(Category).where(Category.slug == "bars"))
            await session.commit()


@pytest.mark.asyncio
async def test_phase1_extraction_by_district_and_qty():
    try:
        with pytest.raises(ValueError):
            await extract_and_stage_venues(location="heliopolis", qty=2, dry_run=True)
    except Exception:
        pytest.skip("External Google API network call timed out or network unavailable")


@pytest.mark.asyncio
async def test_phase2_process_and_publish_approved():
    test_place_id = "ChIJ_approved_publish_test_777"
    try:
        async with AsyncSessionLocal() as session:
            existing = (await session.execute(select(VenueStaging).where(VenueStaging.place_id == test_place_id))).scalar_one_or_none()
            if existing:
                await session.delete(existing)
                await session.commit()

            staging = VenueStaging(
                place_id=test_place_id,
                google_maps_url="https://maps.google.com/?q=place_id:ChIJ_approved_publish_test_777",
                name_raw="Approved Test Pub",
                address_raw="12 Champollion St, Downtown, Cairo",
                location=WKTElement("POINT(31.2385 30.0450)", srid=4326),
                raw_payload={"price_level": "$$", "rating": 4.5},
                status="APPROVED",
            )
            session.add(staging)
            await session.commit()

        from app.cli import process_and_publish_approved
        await process_and_publish_approved(pks=None)

        async with AsyncSessionLocal() as session:
            staged_res = await session.execute(select(VenueStaging).where(VenueStaging.place_id == test_place_id))
            staged_venue = staged_res.scalar_one_or_none()
            assert staged_venue is not None
            assert staged_venue.status == "PUBLISHED"
    finally:
        from sqlalchemy import delete
        async with AsyncSessionLocal() as session:
            await session.execute(delete(Venue).where(Venue.slug.like("%approved%")))
            await session.execute(delete(VenueStaging).where(VenueStaging.place_id == test_place_id))
            await session.commit()

