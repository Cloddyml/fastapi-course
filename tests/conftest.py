# ruff: noqa: E402
import json
from typing import AsyncGenerator
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import ASGITransport, AsyncClient

import app.models  # noqa: F401
from app.api.dependencies import get_db
from app.config import settings
from app.database import Base, async_session_maker_null_pool, engine_null_pool
from app.main import app
from app.schemas.hotels import HotelAdd
from app.schemas.rooms import RoomAdd
from app.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        print("Привет. Я перезаписан")
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    # print("Я ФИКСТУРА")

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)
    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    await ac.post(
        "/auth/register",
        json={"email": "kot@pes.com", "password": "1234"},
    )


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    await ac.post(
        "/auth/login",
        json={"email": "kot@pes.com", "password": "1234"},
    )
    assert ac.cookies["access_token"]
    yield ac
