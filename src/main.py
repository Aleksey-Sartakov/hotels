from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.routing import Mount

from src.api.auth import auth_router
from src.api.bookings import bookings_router
from src.api.facilities import facilities_router
from src.api.hotels import hotels_router
from src.api.rooms import rooms_router
from src.config import settings
from src.connectors.redis_conn import init_redis


sys.path.append(str(Path(__file__).parent.parent))


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_manager = await init_redis(settings.REDIS_HOST, settings.REDIS_PORT)
    app.state.redis = redis_manager
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")

    yield

    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
