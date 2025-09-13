from typing import Annotated

from fastapi import Depends, Request, HTTPException, status
from pydantic import BaseModel, Field

from src.services.auth import AuthService


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


PaginationDep = Annotated[Pagination, Depends()]
UserIdDep = Annotated[get_current_user_id, Depends()]
