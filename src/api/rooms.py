from fastapi import APIRouter, Body
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest


rooms_router = APIRouter(prefix="/hotels", tags=["Номера"])


@rooms_router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep):
    rooms = await db.rooms.get_all(hotel_id)

    return rooms


@rooms_router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)

    return room


@rooms_router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_rooms(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "No content"}


@rooms_router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body(openapi_examples={
    "1": Example(summary="Люкс, отель 1", value={
        "hotel_id": 1,
        "title": "Люкс",
        "description": "Супер пупер номер",
        "price": 12000,
        "quantity": 2
    }),
    "2": Example(summary="Средний, отель 1", value={
        "hotel_id": 1,
        "title": "Средний",
        "description": "Ничего необычного",
        "price": 6000,
        "quantity": 33
    }),
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "Created", "data": room}


@rooms_router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomPatch, db: DBDep):
    await db.rooms.edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "No content"}


@rooms_router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(hotel_id: int, room_id: int, room_data: RoomAdd, db: DBDep):
    await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "No content"}
