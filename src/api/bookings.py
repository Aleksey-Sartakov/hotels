from fastapi import APIRouter, Body, HTTPException, status
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd


bookings_router = APIRouter(prefix="/bookings", tags=["Бронирования"])


# @rooms_router.get("/{hotel_id}/rooms")
# async def get_rooms(hotel_id: int, db: DBDep):
#     rooms = await db.rooms.get_all(hotel_id)
#
#     return rooms
#
#
# @rooms_router.get("/{hotel_id}/rooms/{room_id}")
# async def get_room(hotel_id: int, room_id: int, db: DBDep):
#     room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
#
#     return room
#
#
# @rooms_router.delete("/{hotel_id}/rooms/{room_id}")
# async def delete_rooms(hotel_id: int, room_id: int, db: DBDep):
#     await db.rooms.delete(id=room_id, hotel_id=hotel_id)
#     await db.commit()
#
#     return {"status": "No content"}


@bookings_router.post("/")
async def create_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest = Body(openapi_examples={
    "1": Example(summary="Бронирование 1", value={
        "date_from": "2026-01-01",
        "date_to": "2026-01-10",
        "room_id": 2
    }),
    "2": Example(summary="Бронирование 2", value={
        "date_from": "2026-01-01",
        "date_to": "2026-01-03",
        "room_id": 3
    }),
    "3": Example(summary="Бронирование запрещенное", value={
        "date_from": "2026-01-01",
        "date_to": "2026-01-03",
        "room_id": 1
    }),
})):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Выбранная комната не существует!")

    _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump(exclude_unset=True))
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "Created", "data": booking}


# @rooms_router.patch("/{hotel_id}/rooms/{room_id}")
# async def patch_room(hotel_id: int, room_id: int, room_data: RoomPatch, db: DBDep):
#     await db.rooms.edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
#     await db.commit()
#
#     return {"status": "No content"}
#
#
# @rooms_router.put("/{hotel_id}/rooms/{room_id}")
# async def put_room(hotel_id: int, room_id: int, room_data: RoomAdd, db: DBDep):
#     await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)
#     await db.commit()
#
#     return {"status": "No content"}
