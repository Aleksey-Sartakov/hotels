from pydantic import Field

from src.schemas.base import BaseSchema


class HotelAdd(BaseSchema):
    location: str
    title: str


class Hotel(HotelAdd):
    id: int


class HotelPatch(BaseSchema):
    location: str | None = None
    title: str | None = None
