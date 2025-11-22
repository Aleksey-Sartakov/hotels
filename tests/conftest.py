import json
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.utils.db_manager import DBManager


async def get_db_null_pool() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture()
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            yield ac


@pytest.fixture(scope="session")
async def insert_data_in_db(setup_database, ac):
    with open("tests/mock_hotels.json", "r", encoding="utf-8") as hotels_f:
        hotels_data = json.load(hotels_f)
        for hotel in hotels_data:
            await ac.post("/hotels", json=hotel)

        with open("tests/mock_rooms.json", "r", encoding="utf-8") as rooms_f:
            rooms_data = json.load(rooms_f)
            for room in rooms_data:
                await ac.post(f"/hotels/{room['hotel_id']}/rooms", json=room)


@pytest.fixture(scope="session", autouse=True)
async def register_user(insert_data_in_db, ac):
    await ac.post("/auth/register", json={"email": "test@user.com", "password": "1234"})
