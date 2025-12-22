from src.schemas.base import BaseSchema, NonEmptyPayloadSchema


class HotelAdd(BaseSchema):
    location: str
    title: str


class Hotel(HotelAdd):
    id: int


class HotelPatch(NonEmptyPayloadSchema):
    location: str | None = None
    title: str | None = None
