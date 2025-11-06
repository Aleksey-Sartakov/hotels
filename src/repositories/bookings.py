from datetime import date

from sqlalchemy import select

from src.models.bookings import Bookings
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = Bookings
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(Bookings)
            .filter(Bookings.date_from == date.today())
        )
        res = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars()]
