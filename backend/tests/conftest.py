import pytest
from app.core.database import engine


@pytest.fixture(autouse=True)
async def reset_engine_connections():
    await engine.dispose()
    yield
    await engine.dispose()
