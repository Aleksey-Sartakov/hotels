from datetime import date

from sqlalchemy import select, func

from src.models.bookings import Bookings
from src.models.rooms import Rooms


def get_available_rooms_ids_query(date_from: date, date_to: date):
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

    return available_rooms_ids
