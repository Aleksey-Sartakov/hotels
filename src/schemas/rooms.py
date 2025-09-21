from src.schemas.base import BaseSchema
from src.schemas.facilities import Facility


class RoomAddRequest(BaseSchema):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None = None


class RoomAdd(BaseSchema):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatch(BaseSchema):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomPatchRequest(RoomPatch):
    facilities_ids: list[int] | None = None
