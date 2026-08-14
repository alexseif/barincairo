import uuid
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, select

from app.cli import create_admin_user
from app.core.database import AsyncSessionLocal
from app.main import app
from app.models.venue_staging import VenueStaging
from app.models.venues import Category, Venue, VibeTag


async def get_authenticated_client() -> AsyncClient:
    """Helper to return an authenticated httpx AsyncClient for SQLAdmin testing."""
    await create_admin_user("admin@barincairo.com", "supersecretadmin")
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://testserver")
    login_res = await client.post(
        "/admin/login",
        data={"username": "admin@barincairo.com", "password": "supersecretadmin"},
        follow_redirects=True,
    )
    assert login_res.status_code == 200
    return client


@pytest.mark.asyncio
async def test_admin_all_list_views():
    """Verify that all registered admin list views return 200 OK without 500 errors."""
    client = await get_authenticated_client()
    routes = [
        "/admin/user/list",
        "/admin/category/list",
        "/admin/vibe-tag/list",
        "/admin/venue/list",
        "/admin/venue-staging/list",
        "/admin/venue-photo/list",
        "/admin/subscriber/list",
    ]
    for route in routes:
        response = await client.get(route)
        assert response.status_code == 200, f"Route {route} failed with {response.status_code}: {response.text}"
    await client.aclose()


@pytest.mark.asyncio
async def test_admin_category_crud():
    """Test Category list, create GET, create POST, and details."""
    test_slug = f"test-cat-{uuid.uuid4().hex[:6]}"
    async with AsyncSessionLocal() as session:
        await session.execute(delete(Category).where(Category.slug == test_slug))
        await session.commit()

    client = await get_authenticated_client()

    # GET create form
    create_form_res = await client.get("/admin/category/create")
    assert create_form_res.status_code == 200

    # POST create Category
    post_res = await client.post(
        "/admin/category/create",
        data={"slug": test_slug, "name": "Admin Test Category"},
        follow_redirects=True,
    )
    assert post_res.status_code == 200

    # Verify category in DB
    async with AsyncSessionLocal() as session:
        cat_res = await session.execute(select(Category).where(Category.slug == test_slug))
        cat = cat_res.scalar_one_or_none()
        assert cat is not None
        assert cat.name == "Admin Test Category"
        cat_id = cat.id

    # GET detail view
    detail_res = await client.get(f"/admin/category/details/{cat_id}")
    assert detail_res.status_code == 200
    await client.aclose()


@pytest.mark.asyncio
async def test_admin_vibe_tag_crud():
    """Test VibeTag list, create GET, create POST, and details."""
    test_slug = f"test-vibe-{uuid.uuid4().hex[:6]}"
    async with AsyncSessionLocal() as session:
        await session.execute(delete(VibeTag).where(VibeTag.slug == test_slug))
        await session.commit()

    client = await get_authenticated_client()

    create_form_res = await client.get("/admin/vibe-tag/create")
    assert create_form_res.status_code == 200

    post_res = await client.post(
        "/admin/vibe-tag/create",
        data={"slug": test_slug, "name": "Admin Test Vibe"},
        follow_redirects=True,
    )
    assert post_res.status_code == 200

    async with AsyncSessionLocal() as session:
        vibe_res = await session.execute(select(VibeTag).where(VibeTag.slug == test_slug))
        vibe = vibe_res.scalar_one_or_none()
        assert vibe is not None
        assert vibe.name == "Admin Test Vibe"
        vibe_id = vibe.id

    detail_res = await client.get(f"/admin/vibe-tag/details/{vibe_id}")
    assert detail_res.status_code == 200
    await client.aclose()


@pytest.mark.asyncio
async def test_admin_venue_crud_and_spatial_helpers():
    """Test Venue list, create form GET, create POST with lat/lng, and details view."""
    test_slug = f"test-venue-{uuid.uuid4().hex[:6]}"
    async with AsyncSessionLocal() as session:
        await session.execute(delete(Venue).where(Venue.slug == test_slug))
        await session.commit()

    client = await get_authenticated_client()

    # GET create form
    create_form_res = await client.get("/admin/venue/create")
    assert create_form_res.status_code == 200

    # Fetch a valid category ID to link
    async with AsyncSessionLocal() as session:
        cat_res = await session.execute(select(Category))
        cat = cat_res.scalars().first()
        assert cat is not None
        category_id = str(cat.id)

    # POST create Venue with lat/lng
    post_res = await client.post(
        "/admin/venue/create",
        data={
            "slug": test_slug,
            "name": "Admin Test Venue",
            "description": "Test description",
            "address": "10 Talaat Harb, Downtown",
            "working_hours": "5:00 PM - 2:00 AM",
            "google_maps_url": "https://maps.google.com/?q=place_id:ChIJ999",
            "price_range": "$$",
            "vibe_description": "Test vibe",
            "photo_url": "https://example.com/photo.jpg",
            "is_active": "true",
            "category": category_id,
            "latitude": "30.0450",
            "longitude": "31.2380",
        },
        follow_redirects=True,
    )
    assert post_res.status_code == 200, f"Failed with: {post_res.text}"

    # Verify Venue created in DB with correct lat/lng properties
    async with AsyncSessionLocal() as session:
        v_res = await session.execute(select(Venue).where(Venue.slug == test_slug))
        venue = v_res.scalar_one_or_none()
        assert venue is not None
        assert venue.name == "Admin Test Venue"
        assert venue.working_hours == "5:00 PM - 2:00 AM"
        assert venue.latitude == 30.0450
        assert venue.longitude == 31.2380
        venue_id = venue.id

    # GET detail view
    detail_res = await client.get(f"/admin/venue/details/{venue_id}")
    assert detail_res.status_code == 200
    await client.aclose()


@pytest.mark.asyncio
async def test_admin_venue_staging_crud():
    """Test VenueStaging list, create form GET, create POST, and details view."""
    test_place_id = f"ChIJ_admin_staging_{uuid.uuid4().hex[:6]}"
    async with AsyncSessionLocal() as session:
        await session.execute(delete(VenueStaging).where(VenueStaging.place_id == test_place_id))
        await session.commit()

    client = await get_authenticated_client()

    create_form_res = await client.get("/admin/venue-staging/create")
    assert create_form_res.status_code == 200

    post_res = await client.post(
        "/admin/venue-staging/create",
        data={
            "place_id": test_place_id,
            "google_maps_url": "https://maps.google.com/?q=place_id:ChIJ_admin_staging_999",
            "name_raw": "Admin Staging Bar",
            "address_raw": "5 Champollion St",
            "working_hours": "6:00 PM - 3:00 AM",
            "status": "PENDING_CURATION",
            "raw_payload": "{}",
            "latitude": "30.0460",
            "longitude": "31.2390",
        },
        follow_redirects=True,
    )
    assert post_res.status_code == 200, f"Failed with: {post_res.text}"

    # Verify record created in DB
    async with AsyncSessionLocal() as session:
        s_res = await session.execute(select(VenueStaging).where(VenueStaging.place_id == test_place_id))
        staging = s_res.scalar_one_or_none()
        assert staging is not None
        assert staging.name_raw == "Admin Staging Bar"
        assert staging.working_hours == "6:00 PM - 3:00 AM"
        assert staging.latitude == 30.0460
        assert staging.longitude == 31.2390
        staging_id = staging.id

    detail_res = await client.get(f"/admin/venue-staging/details/{staging_id}")
    assert detail_res.status_code == 200
    await client.aclose()
