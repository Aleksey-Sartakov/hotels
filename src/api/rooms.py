from fastapi import APIRouter, Body
from fastapi.openapi.models import Example

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest

ROOMS_ROUTER_TAGS = ["Номера"]


rooms_router = APIRouter(prefix="/{hotel_id}/rooms")


@rooms_router.get("/", tags=ROOMS_ROUTER_TAGS)
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        rooms_repository = RoomsRepository(session)
        rooms = await rooms_repository.get_all(hotel_id)

        return rooms


@rooms_router.get("/{room_id}", tags=ROOMS_ROUTER_TAGS)
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        rooms_repository = RoomsRepository(session)
        room = await rooms_repository.get_one_or_none(id=room_id, hotel_id=hotel_id)

        return room


@rooms_router.delete("/{room_id}", tags=ROOMS_ROUTER_TAGS)
async def delete_rooms(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        rooms_repository = RoomsRepository(session)
        await rooms_repository.delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {"status": "No content"}


@rooms_router.post("/", tags=ROOMS_ROUTER_TAGS)
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
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
    async with async_session_maker() as session:
        rooms_repository = RoomsRepository(session)
        room = await rooms_repository.add(_room_data)
        await session.commit()

    return {"status": "Created", "data": room}


@rooms_router.patch("/{room_id}", tags=ROOMS_ROUTER_TAGS)
async def patch_room(hotel_id: int, room_id: int, room_data: RoomPatch):
    async with async_session_maker() as session:
        rooms_repository = RoomsRepository(session)
        await rooms_repository.edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {"status": "No content"}


@rooms_router.put("/{room_id}", tags=ROOMS_ROUTER_TAGS)
async def put_room(hotel_id: int, room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        rooms_repository = RoomsRepository(session)
        await rooms_repository.edit(room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {"status": "No content"}
