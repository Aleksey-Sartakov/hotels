from datetime import date

from src.schemas.base import BaseSchema, NonEmptyPayloadSchema


class BookingAddRequest(BaseSchema):
    date_from: date
    date_to: date
    room_id: int


class BookingAdd(BookingAddRequest):
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int
    total_cost: int


class BookingUpdate(NonEmptyPayloadSchema):
    date_from: date | None = None
    date_to: date | None = None
    room_id: int | None = None
    price: int | None = None
