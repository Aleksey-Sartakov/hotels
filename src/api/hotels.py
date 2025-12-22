from datetime import date

from fastapi import APIRouter, Body
from fastapi.openapi.models import Example
from fastapi.params import Query
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import DateToLessOrEqualThenDateFromException, HotelNotFoundHTTPException, HotelNotFoundException, \
    DateCannotBeInPastException, DateCannotBeInPastHTTPException, BookingDateToLessOrEqualThenDateFromHTTPException
from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.hotels import HotelService

hotels_router = APIRouter(prefix="/hotels", tags=["Отели"])


@hotels_router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date = Query(example="2026-01-01"),
    date_to: date = Query(example="2026-01-20"),
    location: str | None = Query(None, description="Расположение отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
    hotel_service = HotelService(db)

    try:
        hotels = await hotel_service.get_filtered_by_time(
            pagination=pagination, date_from=date_from, date_to=date_to, location=location, title=title
        )
    except DateToLessOrEqualThenDateFromException:
        raise BookingDateToLessOrEqualThenDateFromHTTPException
    except DateCannotBeInPastException:
        raise DateCannotBeInPastHTTPException

    return hotels


@hotels_router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    hotel_service = HotelService(db)

    try:
        hotel = await hotel_service.get_hotel(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return hotel


@hotels_router.delete("/{hotel_id}")
async def delete_hotels(hotel_id: int, db: DBDep):
    hotel_service = HotelService(db)
    try:
        await hotel_service.delete_hotel(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "No content"}


@hotels_router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": Example(summary="Дубай", value={"location": "Дубай ул. Шейха 11", "title": "Топ-1 хотель"}),
            "2": Example(
                summary="Сочи", value={"location": "Сочи ул. Красной поляны 22", "title": "Супер дупер отель"}
            ),
        }
    ),
):
    hotel_service = HotelService(db)
    hotel = await hotel_service.add_hotel(hotel_data)

    return {"status": "Created", "data": hotel}


@hotels_router.patch("/{hotel_id}")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    hotel_service = HotelService(db)
    await hotel_service.patch_hotel(hotel_id, hotel_data)

    return {"status": "No content"}


@hotels_router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    hotel_service = HotelService(db)
    await hotel_service.put_hotel(hotel_id, hotel_data)

    return {"status": "No content"}
