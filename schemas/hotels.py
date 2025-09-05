from pydantic import BaseModel, Field


class Hotel(BaseModel):
    name: str
    title: str


class HotelPatch(BaseModel):
    name: str | None = Field(default=None)
    title: str | None = Field(default=None)