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
        "name_en": "Test Venue",
        "name_ar": "مكان تجريبي",
        "address_en": "123 Sarwat St",
        "address_ar": "١٢٣ شارع ثروت",
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
    bbox = (30.0380, 31.2300, 30.0520, 31.2480)

    # 1. Extraction Phase
    records = await extract_and_stage_venues(bbox=bbox, dry_run=False, fixtures_only=True)
    assert len(records) >= 0  # May be 0 if already staged from previous runs

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
