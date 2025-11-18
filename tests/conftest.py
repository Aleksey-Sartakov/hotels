import json

import pytest
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def insert_data_in_db(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        with open("tests/mock_hotels.json", "r") as hotels_f:
            hotels_data = json.loads(hotels_f.read())
            for hotel in hotels_data:
                response = await ac.post(
                    "/hotels",
                    json=hotel
                )

        with open("tests/mock_rooms.json", "r") as rooms_f:
            rooms_data = json.loads(rooms_f.read())
            for room in rooms_data:
                await ac.post(
                    f"/hotels/{room['hotel_id']}/rooms",
                    json=room
                )


@pytest.fixture(scope="session", autouse=True)
async def register_user(insert_data_in_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/auth/register",
            json={"email": "test@user.com", "password": "1234"}
        )
