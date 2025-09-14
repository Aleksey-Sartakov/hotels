from src.schemas.base import BaseSchema


class RoomAddRequest(BaseSchema):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomAdd(RoomAddRequest):
    hotel_id: int


class Room(RoomAdd):
    id: int


class RoomPatch(BaseSchema):
    title: str | None = None
    description: str | None = None
    price: str | None = None
    quantity: str | None = None
