from sqlalchemy import select

from src.models.rooms import Rooms
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = Rooms
    schema = Room

    async def get_all(self, hotel_id: int) -> list[schema]:
        query = select(self.model).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)

        return [self.schema.model_validate(hotel) for hotel in result.scalars().all()]
