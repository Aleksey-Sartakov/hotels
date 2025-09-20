from datetime import date

from sqlalchemy import select, func

from src.models.bookings import Bookings
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

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_count = (
            select(Bookings.room_id, func.count("*").label("rooms_booked"))
            .select_from(Bookings)
            .filter(
                Bookings.date_from <= date_to,
                Bookings.date_to >= date_from
            )
            .group_by(Bookings.room_id)
            .cte("rooms_count")
        )
        rooms_left_table = (
            select(
                Rooms.id.label("room_id"),
                (Rooms.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left")
            )
            .outerjoin(rooms_count, Rooms.id == rooms_count.c.room_id)
            .cte("rooms_left_table")
        )
        available_rooms_ids = (
            select(rooms_left_table.c.room_id)
            .filter(rooms_left_table.c.rooms_left > 0)
        )
        query = (
            select(Rooms)
            .filter(Rooms.hotel_id == hotel_id, Rooms.id.in_(available_rooms_ids))
        )
        result = await self.session.execute(query)
        print(query.compile(compile_kwargs={"literal_binds": True}))

        return [self.schema.model_validate(entity) for entity in result.scalars().all()]
