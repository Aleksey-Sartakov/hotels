import json
from typing import AsyncGenerator
from unittest import mock
from unittest.mock import AsyncMock

from sqlalchemy import True_

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from fastapi import Request
from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db, get_redis
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.utils.db_manager import DBManager


# Функция для переопределения зависимости к БД, чтобы создавалось соединение без пула - нужно т.к. каждый тест вызывается в отдельном процессе
async def get_db_null_pool() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

# Функция для переопределения зависимости с redis - по умолчанию при тестах не срабатывает lifespan, поэтому нам неоткуда достать объект редис
async def fake_get_redis(request: Request):
    return AsyncMock()

app.dependency_overrides[get_db] = get_db_null_pool
app.dependency_overrides[get_redis] = fake_get_redis


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


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    # Явно вызываем срабатывание lifespan, без этого он не отработает по умолчанию
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


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    response = await ac.post("/auth/login", json={"email": "test@user.com", "password": "1234"})
    assert response.status_code == 200
    assert ac.cookies["access_token"]

    yield ac
