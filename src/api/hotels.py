from fastapi import APIRouter, Body
from fastapi.openapi.models import Example
from fastapi.params import Query
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import Hotels
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

    async with async_session_maker() as session:
        query = select(Hotels)
        if location:
            query = query.filter(Hotels.location.icontains(location))
        if title:
            query = query.filter(Hotels.title.icontains(title))
        query = (
            query
            .limit(limit)
            .offset((pagination.page - 1) * limit)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()

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
        add_hotel_stmt = insert(Hotels).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "Created"}


@hotels_router.patch("/{hotel_id}")
def patch_hotel(hotel_id: int, hotel_data: HotelPatch):


    return {"status": "Not found"}


@hotels_router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):

    return {"status": "Not found"}

