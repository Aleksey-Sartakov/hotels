from pydantic import Field

from src.schemas.base import BaseSchema


class RoomAdd(BaseSchema):
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


class RoomPatch(BaseSchema):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: str | None = Field(default=None)
    quantity: str | None = Field(default=None)
