import pytest
from pydantic import ValidationError

from app.schemas.venue_staging import VenueIngestSchema


def test_valid_venue_ingest_schema():
    valid_payload = {
        "slug": "cap-d-or",
        "category_slug": "bars",
        "name_en": "Cap d'Or",
        "name_ar": "كاب دي أور",
        "description_en": "Historic Downtown watering hole.",
        "description_ar": "بار تاريخي في وسط البلد.",
        "address_en": "Abdel Khalek Sarwat St, Downtown",
        "address_ar": "شارع عبد الخالق ثروت، وسط البلد",
        "google_maps_url": "https://maps.google.com/?q=place_id:ChIJ12345",
        "latitude": 30.0450,
        "longitude": 31.2380,
        "price_range": "$$",
        "vibe_description": "Retro, artistic, nostalgic",
        "photo_url": "https://example.com/photos/hero.jpg",
        "gallery_photos": ["https://example.com/photos/1.jpg"],
        "vibes": ["historic", "cozy"],
        "citations": [
            "Cairo: The City Victorious by Max Rodenbeck, p. 142",
            "Al-Ahram Weekly Archival Feature 1998",
        ],
    }

    schema = VenueIngestSchema(**valid_payload)
    assert schema.slug == "cap-d-or"
    assert schema.latitude == 30.0450
    assert len(schema.citations) == 2


def test_rejected_fewer_than_2_citations():
    invalid_payload = {
        "slug": "cap-d-or",
        "category_slug": "bars",
        "name_en": "Cap d'Or",
        "name_ar": "كاب دي أور",
        "address_en": "Abdel Khalek Sarwat St",
        "address_ar": "شارع عبد الخالق ثروت",
        "google_maps_url": "https://maps.google.com/?q=place_id:ChIJ12345",
        "latitude": 30.0450,
        "longitude": 31.2380,
        "photo_url": "https://example.com/photos/hero.jpg",
        "citations": ["Single citation only"],
    }

    with pytest.raises(ValidationError) as excinfo:
        VenueIngestSchema(**invalid_payload)
    assert "citations" in str(excinfo.value)


def test_rejected_outside_bounding_box():
    # Outside Downtown Cairo lat: 31.0000 (North of Cairo)
    invalid_payload = {
        "slug": "cap-d-or",
        "category_slug": "bars",
        "name_en": "Cap d'Or",
        "name_ar": "كاب دي أور",
        "address_en": "Abdel Khalek Sarwat St",
        "address_ar": "شارع عبد الخالق ثروت",
        "google_maps_url": "https://maps.google.com/?q=place_id:ChIJ12345",
        "latitude": 31.0000,
        "longitude": 31.2380,
        "photo_url": "https://example.com/photos/hero.jpg",
        "citations": ["Citation 1", "Citation 2"],
    }

    with pytest.raises(ValidationError) as excinfo:
        VenueIngestSchema(**invalid_payload)
    assert "latitude" in str(excinfo.value)
