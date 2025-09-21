from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.models.rooms import Rooms
from src.repositories.base import BaseRepository
from src.repositories.utils import get_available_rooms_ids_query
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = Rooms
    schema = Room

    async def get_all(self, hotel_id: int) -> list[schema]:
        query = select(self.model).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)

        return [self.schema.model_validate(hotel) for hotel in result.scalars().all()]

    async def get_filtered_by_period(self, hotel_id: int, date_from: date, date_to: date):
        available_rooms_ids = get_available_rooms_ids_query(date_from, date_to)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(Rooms.hotel_id == hotel_id, Rooms.id.in_(available_rooms_ids))
        )
        result = await self.session.execute(query)

        return [RoomWithRels.model_validate(entity) for entity in result.unique().scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        entity = result.scalars().one_or_none()
        if entity:
            entity = RoomWithRels.model_validate(entity)

        return entity
