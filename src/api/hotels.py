from fastapi import APIRouter, Body
from fastapi.openapi.models import Example
from fastapi.params import Query
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import Hotels
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPatch


hotels_router = APIRouter(prefix="/hotels", tags=["Отели"])

HOTELS_GET_LIMIT = 5


@hotels_router.get("/")
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


@hotels_router.delete("/{hotel_id}")
def delete_hotels(
        hotel_id: int
):

    return {"status": "No content"}


@hotels_router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
        hotel = await hotels_repository.add(**hotel_data.model_dump())
        await session.commit()

    return {"status": "Created", "data": hotel}


@hotels_router.patch("/{hotel_id}")
def patch_hotel(hotel_id: int, hotel_data: HotelPatch):


    return {"status": "Not found"}


@hotels_router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):

    return {"status": "Not found"}

