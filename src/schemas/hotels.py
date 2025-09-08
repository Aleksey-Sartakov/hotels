from pydantic import BaseModel, Field

from src.schemas.base import BaseSchema


class HotelAdd(BaseSchema):
    location: str
    title: str


class Hotel(HotelAdd):
    id: int


class HotelPatch(BaseSchema):
    location: str | None = Field(default=None)
    title: str | None = Field(default=None)