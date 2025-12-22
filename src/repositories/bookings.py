from datetime import date

from fastapi import HTTPException
from sqlalchemy import select

from src.exceptions import AllRoomsAreBookedException, DateCannotBeInPastException, \
    DateToLessOrEqualThenDateFromException
from src.models.bookings import Bookings
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import get_available_rooms_ids_query
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = Bookings
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(Bookings).filter(Bookings.date_from == date.today())
        res = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars()]

    async def add_booking(self, data: BookingAdd):
        today = date.today()
        if data.date_from < today or data.date_to < today:
            raise DateCannotBeInPastException
        if data.date_from >= data.date_to:
            raise DateToLessOrEqualThenDateFromException

        available_rooms_ids_query = get_available_rooms_ids_query(data.date_from, data.date_to)
        available_rooms_ids = await self.session.execute(available_rooms_ids_query)
        if data.room_id not in available_rooms_ids.scalars():
            raise AllRoomsAreBookedException()

        booking = await self.add(data)

        return booking
