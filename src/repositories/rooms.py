from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.models.rooms import Rooms
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomWithRelsDataMapper
from src.repositories.utils import get_available_rooms_ids_query


class RoomsRepository(BaseRepository):
    model = Rooms
    mapper = RoomDataMapper

    async def get_filtered_by_period(self, hotel_id: int, date_from: date, date_to: date):
        available_rooms_ids = get_available_rooms_ids_query(date_from, date_to)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(Rooms.hotel_id == hotel_id, Rooms.id.in_(available_rooms_ids))
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return [RoomWithRelsDataMapper.map_to_domain_entity(entity) for entity in result.unique().scalars().all()]

    async def get_one_or_none_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        entity = result.scalars().one_or_none()
        if entity:
            entity = RoomWithRelsDataMapper.map_to_domain_entity(entity)

        return entity
