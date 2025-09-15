from datetime import date

from src.schemas.base import BaseSchema


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
