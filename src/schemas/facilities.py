from pydantic import Field

from src.schemas.base import BaseSchema


class FacilityAdd(BaseSchema):
    title: str


class Facility(FacilityAdd):
    id: int
