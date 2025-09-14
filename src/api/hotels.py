from fastapi import APIRouter, Body
from fastapi.openapi.models import Example
from fastapi.params import Query

from src.api.dependencies import PaginationDep
from src.api.rooms import rooms_router
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPatch, HotelAdd


HOTELS_GET_LIMIT = 5
HOTELS_ROUTER_TAGS = ["Отели"]


hotels_router = APIRouter(prefix="/hotels")
hotels_router.include_router(rooms_router)


@hotels_router.get("/", tags=HOTELS_ROUTER_TAGS)
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Расположение отеля"),
        title: str | None = Query(None, description="Название отеля")
):
    limit = pagination.per_page or HOTELS_GET_LIMIT
    offset = (pagination.page - 1) * limit

    async with async_session_maker() as session:
        hotels_repository = HotelsRepository(session)
        hotels = await hotels_repository.get_all(location, title, limit, offset)

        return hotels


@hotels_router.get("/{hotel_id}", tags=HOTELS_ROUTER_TAGS)
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotels_repository = HotelsRepository(session)
        hotel = await hotels_repository.get_one_or_none(id=hotel_id)

        return hotel


@hotels_router.delete("/{hotel_id}", tags=HOTELS_ROUTER_TAGS)
async def delete_hotels(hotel_id: int):
    async with async_session_maker() as session:
        hotels_repository = HotelsRepository(session)
        await hotels_repository.delete(id=hotel_id)
        await session.commit()

    return {"status": "No content"}


@hotels_router.post("", tags=HOTELS_ROUTER_TAGS)
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": Example(summary="Дубай", value={
        "location": "Дубай ул. Шейха 11",
        "title": "Топ-1 хотель"
    }),
    "2": Example(summary="Сочи", value={
        "location": "Сочи ул. Красной поляны 22",
        "title": "Супер дупер отель"
    })
})):
    async with async_session_maker() as session:
        hotels_repository = HotelsRepository(session)
        hotel = await hotels_repository.add(hotel_data)
        await session.commit()

    return {"status": "Created", "data": hotel}


@hotels_router.patch("/{hotel_id}", tags=HOTELS_ROUTER_TAGS)
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    async with async_session_maker() as session:
        hotels_repository = HotelsRepository(session)
        await hotels_repository.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return {"status": "No content"}


@hotels_router.put("/{hotel_id}", tags=HOTELS_ROUTER_TAGS)
async def put_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        hotels_repository = HotelsRepository(session)
        await hotels_repository.edit(hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "No content"}
