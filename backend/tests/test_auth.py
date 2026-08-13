import pytest
from httpx import ASGITransport, AsyncClient
from starlette.requests import Request

from app.admin.auth import authentication_backend
from app.core.config import settings
from app.main import app


def test_legacy_env_credentials_removed():
    """Verify that legacy ADMIN_USERNAME and ADMIN_PASSWORD fields are strictly absent from configuration."""
    assert not hasattr(settings, "ADMIN_PASSWORD")
    assert not hasattr(settings, "ADMIN_USERNAME")


@pytest.mark.asyncio
async def test_auth_login_invalid_credentials():
    """Verify that login fails with invalid credentials against the database."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/api/v1/auth/cookie/login",
            data={"username": "invalid@barincairo.com", "password": "wrongpassword"},
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_auth_login_success():
    """Verify that login succeeds for seeded superuser and sets auth cookie."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/api/v1/auth/cookie/login",
            data={"username": "admin@barincairo.com", "password": "supersecretadmin"},
        )
        assert response.status_code in (200, 204)
        assert "barincairo_auth" in response.cookies


@pytest.mark.asyncio
async def test_admin_auth_class():
    """Test SQLAdmin AdminAuth login and authenticate flow."""
    session_store = {}

    # Mock Request for Login Failure
    req_fail = Request({"type": "http", "method": "POST", "headers": [], "session": {}})
    async def mock_form_fail():
        return {"username": "baduser@test.com", "password": "bad"}
    req_fail.form = mock_form_fail

    assert await authentication_backend.login(req_fail) is False

    # Mock Request for Login Success
    req_success = Request({"type": "http", "method": "POST", "headers": [], "session": session_store})
    async def mock_form_success():
        return {"username": "admin@barincairo.com", "password": "supersecretadmin"}
    req_success.form = mock_form_success

    assert await authentication_backend.login(req_success) is True
    assert "token" in session_store

    # Test authenticate success
    req_auth = Request({"type": "http", "session": session_store})
    assert await authentication_backend.authenticate(req_auth) is True

    # Test logout
    assert await authentication_backend.logout(req_auth) is True
    assert "token" not in session_store
