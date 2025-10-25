from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException, status
from fastapi.openapi.models import Example
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomToFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest


rooms_router = APIRouter(prefix="/hotels", tags=["Номера"])


@rooms_router.get("/{hotel_id}/rooms")
@cache(expire=10)
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2026-01-01"),
        date_to: date = Query(example="2026-01-20")
):
    rooms = await db.rooms.get_filtered_by_period(hotel_id, date_from, date_to)

    return rooms


@rooms_router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    room = await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)

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
        "quantity": 2,
        "facilities_ids": []
    }),
    "2": Example(summary="Средний, отель 1", value={
        "hotel_id": 1,
        "title": "Средний",
        "description": "Ничего необычного",
        "price": 6000,
        "quantity": 33,
        "facilities_ids": []
    }),
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    room = await db.rooms.add(_room_data)

    facilities = [RoomToFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    if facilities:
        await db.rooms_to_facilities.add_bulk(facilities)

    await db.commit()

    return {"status": "Created", "data": room}


@rooms_router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    room = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Номер не найден!")

    room_data_dumped = room_data.model_dump(exclude_unset=True)
    room_data_ = RoomPatch(**room_data_dumped)
    await db.rooms.edit(room_data_, exclude_unset=True, id=room_id, hotel_id=hotel_id)

    if "facilities_ids" in room_data_dumped:
        await db.rooms_to_facilities.update_facilities_in_room(
            room_id=room_id, facilities_ids=room_data_dumped["facilities_ids"]
        )

    await db.commit()

    return {"status": "No content"}


@rooms_router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    room = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Номер не найден!")

    room_data_dumped = room_data.model_dump()
    room_data_ = RoomPatch(**room_data_dumped)
    await db.rooms.edit(room_data_, id=room_id, hotel_id=hotel_id)

    await db.rooms_to_facilities.update_facilities_in_room(
        room_id=room_id, facilities_ids=room_data_dumped["facilities_ids"]
    )

    await db.commit()

    return {"status": "No content"}
