from datetime import date

from sqlalchemy import select

from src.models.hotels import Hotels
from src.models.rooms import Rooms
from src.repositories.base import BaseRepository
from src.repositories.utils import get_available_rooms_ids_query
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = Hotels
    schema = Hotel

    async def get_all(self, location, title, limit, offset) -> list[schema]:
        query = select(self.model)
        if location:
            query = query.filter(Hotels.location.icontains(location))
        if title:
            query = query.filter(Hotels.title.icontains(title))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [self.schema.model_validate(hotel) for hotel in result.scalars().all()]

    async def get_filtered_by_period(
            self,
            location: str,
            title: str,
            limit: int,
            offset: int,
            date_from: date,
            date_to: date
    ):
        available_rooms_ids = get_available_rooms_ids_query(date_from, date_to)
        available_hotels_ids = (
            select(Rooms.hotel_id)
            .filter(Rooms.id.in_(available_rooms_ids))
        )

        return await self.get_filtered(Hotels.id.in_(available_hotels_ids))
