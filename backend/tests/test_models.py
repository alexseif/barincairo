import pytest
from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape
from app.models.venues import Category, VibeTag, Venue
from app.models.venue_staging import VenueStaging


def test_category_single_language():
    cat = Category(slug="bars", name="Bars & Pubs")
    assert cat.name == "Bars & Pubs"
    assert not hasattr(cat, "name_en")
    assert not hasattr(cat, "name_ar")


def test_vibe_tag_single_language():
    vibe = VibeTag(slug="live-music", name="Live Music")
    assert vibe.name == "Live Music"
    assert not hasattr(vibe, "name_en")
    assert not hasattr(vibe, "name_ar")


def test_venue_single_language_and_working_hours():
    venue = Venue(
        slug="test-bar",
        name="Test Bar",
        address="123 Downtown St",
        description="A great bar",
        working_hours="5:00 PM - 3:00 AM",
        category_id=1,
        location=WKTElement("POINT(31.2357 30.0444)", srid=4326),
    )
    assert venue.name == "Test Bar"
    assert venue.address == "123 Downtown St"
    assert venue.description == "A great bar"
    assert venue.working_hours == "5:00 PM - 3:00 AM"
    assert not hasattr(venue, "name_en")
    assert not hasattr(venue, "name_ar")
    assert not hasattr(venue, "address_en")
    assert not hasattr(venue, "address_ar")
    assert not hasattr(venue, "description_en")
    assert not hasattr(venue, "description_ar")


def test_venue_lat_lng_properties():
    venue = Venue(
        slug="test-geo",
        name="Test Geo",
        address="123 Geo St",
        category_id=1,
        location=WKTElement("POINT(31.2389 30.0444)", srid=4326),
    )
    assert venue.latitude == pytest.approx(30.0444)
    assert venue.longitude == pytest.approx(31.2389)

    # Test setters
    venue.latitude = 30.0500
    venue.longitude = 31.2400
    assert venue.latitude == pytest.approx(30.0500)
    assert venue.longitude == pytest.approx(31.2400)


def test_venue_staging_working_hours_and_lat_lng():
    staging = VenueStaging(
        place_id="ChIJ12345",
        google_maps_url="https://maps.google.com/?q=30.0444,31.2389",
        name_raw="Raw Name",
        address_raw="Raw Address",
        raw_payload={},
        working_hours="6:00 PM - 2:00 AM",
        location=WKTElement("POINT(31.2389 30.0444)", srid=4326),
    )
    assert staging.working_hours == "6:00 PM - 2:00 AM"
    assert staging.latitude == pytest.approx(30.0444)
    assert staging.longitude == pytest.approx(31.2389)

    staging.latitude = 30.0600
    staging.longitude = 31.2500
    assert staging.latitude == pytest.approx(30.0600)
    assert staging.longitude == pytest.approx(31.2500)
