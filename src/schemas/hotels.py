from pydantic import BaseModel, Field


class Hotel(BaseModel):
    location: str
    title: str


class HotelPatch(BaseModel):
    location: str | None = Field(default=None)
    title: str | None = Field(default=None)