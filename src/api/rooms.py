from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException, status
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomToFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

rooms_router = APIRouter(prefix="/hotels", tags=["Номера"])


@rooms_router.get("/{hotel_id}/rooms")
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

    if room_data_dumped.get("facilities_ids"):
        if not room_data_dumped["facilities_ids"]:
            await db.rooms_to_facilities.delete_facilities(room_id=room_id)
        else:
            current_room_facilities = await db.rooms_to_facilities.get_filtered(room_id=room_id)
            current_room_facilities_ids = set([
                room_to_facility.facility_id for room_to_facility in current_room_facilities
            ])

            facilities_to_delete = current_room_facilities_ids - set(room_data_dumped["facilities_ids"])
            if facilities_to_delete:
                await db.rooms_to_facilities.delete_facilities(room_id=room_id, facilities_ids=facilities_to_delete)

            facilities_to_add = set(room_data_dumped["facilities_ids"]) - current_room_facilities_ids
            if facilities_to_add:
                await db.rooms_to_facilities.add_bulk(
                    [RoomToFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in facilities_to_add]
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

    if not room_data_dumped["facilities_ids"]:
        await db.rooms_to_facilities.delete_facilities(room_id=room_id)
    else:
        current_room_facilities = await db.rooms_to_facilities.get_filtered(room_id=room_id)
        current_room_facilities_ids = set([
            room_to_facility.facility_id for room_to_facility in current_room_facilities
        ])

        facilities_to_delete = current_room_facilities_ids - set(room_data_dumped["facilities_ids"])
        if facilities_to_delete:
            await db.rooms_to_facilities.delete_facilities(room_id=room_id, facilities_ids=facilities_to_delete)

        facilities_to_add = set(room_data_dumped["facilities_ids"]) - current_room_facilities_ids
        if facilities_to_add:
            await db.rooms_to_facilities.add_bulk(
                [RoomToFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in facilities_to_add]
            )

    await db.commit()

    return {"status": "No content"}
