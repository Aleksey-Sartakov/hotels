from typing import Annotated

from fastapi import Depends, Request, HTTPException, status
from pydantic import BaseModel, Field
from redis.asyncio import Redis

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class Pagination(BaseModel):
    page: int = Field(1, ge=1)
    per_page: int | None = Field(None, ge=1, le=100)


def get_access_token(request: Request) -> str:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Для выполнения данного действия необходимо авторизоваться!"
        )

    return access_token


def get_current_user_id(token: str = Depends(get_access_token)) -> int:
    token_data = AuthService().decode_token(token)

    return token_data["user_id"]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


def get_redis(request: Request) -> Redis:
    return request.app.state.redis


DBDep = Annotated[DBManager, Depends(get_db)]
PaginationDep = Annotated[Pagination, Depends()]
UserIdDep = Annotated[int, Depends(get_current_user_id)]
RedisDep = Annotated[Redis, Depends(get_redis)]
