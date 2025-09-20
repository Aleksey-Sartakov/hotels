from datetime import date

from sqlalchemy import select

from src.models.rooms import Rooms
from src.repositories.base import BaseRepository
from src.repositories.utils import get_available_rooms_ids_query
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = Rooms
    schema = Room

    async def get_all(self, hotel_id: int) -> list[schema]:
        query = select(self.model).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)

        return [self.schema.model_validate(hotel) for hotel in result.scalars().all()]

    async def get_filtered_by_period(self, hotel_id: int, date_from: date, date_to: date):
        available_rooms_ids = get_available_rooms_ids_query(date_from, date_to)

        return await self.get_filtered(Rooms.hotel_id == hotel_id, Rooms.id.in_(available_rooms_ids))
