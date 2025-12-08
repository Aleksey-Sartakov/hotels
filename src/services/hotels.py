from datetime import date

from src.exceptions import ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPatch, Hotel
from src.services.base import BaseService


class HotelService(BaseService):
    HOTELS_GET_LIMIT = 5

    async def get_filtered_by_time(
            self,
            pagination,
            date_from: date,
            date_to: date,
            location: str | None,
            title: str | None,
    ):
        limit = pagination.per_page or self.HOTELS_GET_LIMIT
        offset = (pagination.page - 1) * limit

        hotels = await self.db.hotels.get_filtered_by_period(
            location=location, title=title, date_from=date_from, date_to=date_to, limit=limit, offset=offset
        )

        return hotels

    async def get_hotel(self, hotel_id: int):
        hotel = await self.db.hotels.get_one(id=hotel_id)

        return hotel

    async def get_hotel_or_raise(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException

    async def add_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()

        return hotel

    async def patch_hotel(self, hotel_id: int, hotel_data: HotelPatch):
        await self.db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def put_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
