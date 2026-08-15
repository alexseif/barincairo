import pytest
from pydantic import ValidationError

from app.schemas.venues import (
    CategoryBase,
    CategoryResponse,
    GeoJSONFeature,
    GeoJSONFeatureCollection,
    GeoJSONGeometry,
    VibeTagBase,
    VibeTagResponse,
    VenueCreate,
    VenueProperties,
    VenueUpdate,
)


def test_category_schema_valid():
    cat = CategoryBase(slug="bars", name="Bars & Pubs")
    assert cat.slug == "bars"
    assert cat.name == "Bars & Pubs"

    res = CategoryResponse(id=1, slug="bars", name="Bars & Pubs")
    assert res.id == 1


def test_category_schema_invalid_slug():
    with pytest.raises(ValidationError):
        CategoryBase(slug="INVALID SLUG!", name="Bars & Pubs")


def test_vibe_tag_schema_valid():
    tag = VibeTagBase(slug="cozy", name="Cozy")
    assert tag.slug == "cozy"

    res = VibeTagResponse(id=1, slug="cozy", name="Cozy")
    assert res.id == 1


def test_vibe_tag_schema_invalid_slug():
    with pytest.raises(ValidationError):
        VibeTagBase(slug="Cozy Tag!", name="Cozy")


def test_geojson_geometry_valid():
    geom = GeoJSONGeometry(type="Point", coordinates=[31.2380, 30.0450])
    assert geom.type == "Point"
    assert geom.coordinates == [31.2380, 30.0450]


def test_geojson_geometry_invalid_coordinates_length():
    with pytest.raises(ValidationError):
        GeoJSONGeometry(type="Point", coordinates=[31.2380])


def test_geojson_geometry_invalid_latitude_out_of_range():
    with pytest.raises(ValidationError):
        GeoJSONGeometry(type="Point", coordinates=[31.2380, 95.0])


def test_geojson_geometry_invalid_longitude_out_of_range():
    with pytest.raises(ValidationError):
        GeoJSONGeometry(type="Point", coordinates=[200.0, 30.0450])


def test_venue_properties_valid():
    props = VenueProperties(
        id=1,
        slug="cap-d-or",
        name="Cap d'Or",
        description="Historic Downtown watering hole",
        address="28 Abdel Khalek Sarwat St",
        working_hours="5:00 PM - 3:00 AM",
        price_range="$$",
        vibe_description="Retro, artistic",
        photo_url="https://example.com/photo.jpg",
        category_slug="bars",
        category_name="Bars",
        vibes=["historic", "cozy"],
    )
    assert props.slug == "cap-d-or"
    assert props.price_range == "$$"


def test_venue_properties_invalid_price_range():
    with pytest.raises(ValidationError):
        VenueProperties(
            id=1,
            slug="cap-d-or",
            name="Cap d'Or",
            address="28 Abdel Khalek Sarwat St",
            price_range="EXPENSIVE",
            category_slug="bars",
            category_name="Bars",
        )


def test_venue_create_schema_valid():
    venue_create = VenueCreate(
        slug="cap-d-or",
        name="Cap d'Or",
        address="28 Abdel Khalek Sarwat St",
        category_id=1,
        latitude=30.0450,
        longitude=31.2380,
        price_range="$$",
        vibe_ids=[1, 2],
    )
    assert venue_create.slug == "cap-d-or"
    assert venue_create.latitude == 30.0450


def test_venue_update_schema_partial():
    venue_update = VenueUpdate(name="Cap d'Or Updated", price_range="$$$")
    assert venue_update.name == "Cap d'Or Updated"
    assert venue_update.price_range == "$$$"
    assert venue_update.slug is None
