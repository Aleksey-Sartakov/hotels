from copy import copy

from fastapi import APIRouter
from fastapi.params import Query

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPatch


hotels_router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@hotels_router.get("/")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля")
):
    from_index = (pagination.page - 1) * pagination.per_page
    to_index =  pagination.page * pagination.per_page

    if all([id, title]):
        result = [hotel for hotel in hotels if hotel["title"] == title and hotel["id"] == id]
    elif id:
        result = [hotel for hotel in hotels if hotel["id"] == id]
    elif title:
        result = [hotel for hotel in hotels if hotel["title"] == title]
    else:
        result = copy(hotels)

    return result[from_index : to_index]


@hotels_router.delete("/{hotel_id}")
def delete_hotels(
        hotel_id: int
):
    global hotels

    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"status": "No content"}


@hotels_router.post("")
def create_hotel(hotel_data: Hotel):
    global hotels

    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })

    return {"status": "Created"}

@hotels_router.patch("/{hotel_id}")
def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    global hotels

    if not any([hotel_data.title, hotel_data.name]):
        return {"status": "No content"}

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name

            return {"status": "OK", "hotel": hotel}

    return {"status": "Not found"}


@hotels_router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name

            return {"status": "OK", "hotel": hotel}

    return {"status": "Not found"}

