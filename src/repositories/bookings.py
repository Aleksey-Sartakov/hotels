from sqlalchemy import select

from src.models.bookings import Bookings
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = Bookings
    schema = Booking

    async def get_all(self, hotel_id: int) -> list[schema]:
        query = select(self.model).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)

        return [self.schema.model_validate(hotel) for hotel in result.scalars().all()]
