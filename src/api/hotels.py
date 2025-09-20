from datetime import date

from fastapi import APIRouter, Body
from fastapi.openapi.models import Example
from fastapi.params import Query

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd


HOTELS_GET_LIMIT = 5


hotels_router = APIRouter(prefix="/hotels", tags=["Отели"])


@hotels_router.get("/")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        date_from: date = Query(example="2026-01-01"),
        date_to: date = Query(example="2026-01-20"),
        location: str | None = Query(None, description="Расположение отеля"),
        title: str | None = Query(None, description="Название отеля")
):
    limit = pagination.per_page or HOTELS_GET_LIMIT
    offset = (pagination.page - 1) * limit

    hotels = await db.hotels.get_filtered_by_period(
        location=location,
        title=title,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset
    )

    return hotels


@hotels_router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
        hotel = await db.hotels.get_one_or_none(id=hotel_id)

        return hotel


@hotels_router.delete("/{hotel_id}")
async def delete_hotels(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "No content"}


@hotels_router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "1": Example(summary="Дубай", value={
        "location": "Дубай ул. Шейха 11",
        "title": "Топ-1 хотель"
    }),
    "2": Example(summary="Сочи", value={
        "location": "Сочи ул. Красной поляны 22",
        "title": "Супер дупер отель"
    })
})):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "Created", "data": hotel}


@hotels_router.patch("/{hotel_id}")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": "No content"}


@hotels_router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "No content"}
