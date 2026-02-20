import json

import pytest
from httpx import ASGITransport, AsyncClient

import app.models  # noqa: F401
from app.config import settings
from app.database import Base, async_session_maker_null_pool, engine_null_pool
from app.main import app
from app.schemas.hotels import HotelAdd
from app.schemas.rooms import RoomAdd
from app.utils.db_manager import DBManager


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


@pytest.fixture(scope="session", autouse=True)
async def create_hotels(setup_database):
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        with open("tests/mock_hotels.json", "r") as file:
            hotels_data = json.load(file)
        for hotel_data in hotels_data:
            new_hotel_data = await db.hotels.add(HotelAdd(**hotel_data))
            await db.commit()
            print(f"{new_hotel_data=}")


@pytest.fixture(scope="session", autouse=True)
async def create_rooms(setup_database):
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        with open("tests/mock_rooms.json", "r") as file:
            rooms_data = json.load(file)
        for room_data in rooms_data:
            new_room_data = await db.rooms.add(RoomAdd(**room_data))
            await db.commit()
            print(f"{new_room_data=}")
