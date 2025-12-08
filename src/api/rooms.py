from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException, status
from fastapi.openapi.models import Example
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import (
    DateToLessOrEqualThenDateFromException, ObjectNotFoundException,
                            HotelNotFoundHTTPException, RoomNotFoundHTTPException, HotelNotFoundException,
                            RoomNotFoundException
)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

rooms_router = APIRouter(prefix="/hotels", tags=["Номера"])


@rooms_router.get("/{hotel_id}/rooms")
@cache(expire=10)
async def get_rooms(
    hotel_id: int, db: DBDep, date_from: date = Query(example="2026-01-01"), date_to: date = Query(example="2026-01-20")
):
    room_service = RoomService(db)
    try:
        rooms = await room_service.get_filtered_by_time(hotel_id, date_from, date_to)
    except DateToLessOrEqualThenDateFromException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Дата выезда должна быть указаны позднее даты заезда"
        )

    return rooms


@rooms_router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    room_service = RoomService(db)
    try:
        room = await room_service.get_one_with_rels(room_id, hotel_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    return room


@rooms_router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_rooms(hotel_id: int, room_id: int, db: DBDep):
    room_service = RoomService(db)
    try:
        await room_service.delete_room(hotel_id=hotel_id, room_id=room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "No content"}


@rooms_router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": Example(
                summary="Люкс, отель 1",
                value={
                    "hotel_id": 1,
                    "title": "Люкс",
                    "description": "Супер пупер номер",
                    "price": 12000,
                    "quantity": 2,
                    "facilities_ids": [],
                },
            ),
            "2": Example(
                summary="Средний, отель 1",
                value={
                    "hotel_id": 1,
                    "title": "Средний",
                    "description": "Ничего необычного",
                    "price": 6000,
                    "quantity": 33,
                    "facilities_ids": [],
                },
            ),
        }
    ),
):
    room_service = RoomService(db)
    try:
        room = await room_service.create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "Created", "data": room}


@rooms_router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    room_service = RoomService(db)
    try:
        await room_service.patch_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "No content"}


@rooms_router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    room_service = RoomService(db)
    try:
        await room_service.put_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "No content"}
