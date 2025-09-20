from pydantic import Field

from src.schemas.base import BaseSchema


class FacilityAdd(BaseSchema):
    title: str


class Facility(FacilityAdd):
    id: int


class RoomToFacilityAdd(BaseSchema):
    room_id: int
    facility_id: int


class RoomToFacility(RoomToFacilityAdd):
    id: int
