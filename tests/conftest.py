import pytest
from httpx import ASGITransport, AsyncClient

import app.models  # noqa: F401
from app.config import settings
from app.database import Base, engine_null_pool
from app.main import app


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    print("Я ФИКСТУРА")

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post(
            "/auth/register",
            json={"email": "kot@pes.com", "password": "1234"},
        )
