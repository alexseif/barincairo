import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


@pytest.mark.asyncio
async def test_venues_geojson_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/venues")
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "FeatureCollection"
        assert "features" in data
        assert isinstance(data["features"], list)


@pytest.mark.asyncio
async def test_subscriber_creation_validation():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Invalid payload (short phone number)
        bad_res = await client.post("/api/v1/subscribers", json={"whatsapp_number": "123"})
        assert bad_res.status_code == 422


@pytest.mark.asyncio
async def test_categories_cache_control_header():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/categories")
        assert response.status_code == 200
        assert "cache-control" in response.headers
        assert "max-age=3600" in response.headers["cache-control"]


@pytest.mark.asyncio
async def test_vibes_cache_control_header():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/vibes")
        assert response.status_code == 200
        assert "cache-control" in response.headers
        assert "max-age=3600" in response.headers["cache-control"]


@pytest.mark.asyncio
async def test_venues_bbox_filter():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Cairo area bounding box: min_lng,min_lat,max_lng,max_lat
        bbox_str = "31.1,29.9,31.4,30.2"
        response = await client.get(f"/api/v1/venues?bbox={bbox_str}")
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "FeatureCollection"


@pytest.mark.asyncio
async def test_venues_invalid_bbox():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/venues?bbox=invalid,coords")
        assert response.status_code == 400
        assert "Invalid bbox format" in response.json()["detail"]

