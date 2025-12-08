from datetime import date

from src.exceptions import ObjectNotFoundException, HotelNotFoundException, RoomNotFoundException
from src.schemas.facilities import RoomToFacilityAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch, Room
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        rooms = await self.db.rooms.get_filtered_by_period(hotel_id, date_from, date_to)

        return rooms

    async def get_one_with_rels(self, room_id: int, hotel_id: int):
        room = await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)

        return room

    async def get_room_or_raise(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

    async def create_room(
            self,
            hotel_id: int,
            room_data: RoomAddRequest
    ):
        hotel_service = HotelService(self.db)
        await hotel_service.get_hotel_or_raise(hotel_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
        room = await self.db.rooms.add(_room_data)

        if room_data.facilities_ids:
            facilities = [RoomToFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
            await self.db.rooms_to_facilities.add_bulk(facilities)

        await self.db.commit()

    async def patch_room(self, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
        hotel_service = HotelService(self.db)
        await hotel_service.get_hotel_or_raise(hotel_id)

        await self.get_room_or_raise(room_id)

        room_data_dumped = room_data.model_dump(exclude_unset=True)
        room_data_ = RoomPatch(**room_data_dumped)
        await self.db.rooms.edit(room_data_, exclude_unset=True, id=room_id, hotel_id=hotel_id)

        if "facilities_ids" in room_data_dumped:
            await self.db.rooms_to_facilities.update_facilities_in_room(
                room_id=room_id, facilities_ids=room_data_dumped["facilities_ids"]
            )

        await self.db.commit()

    async def put_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequest):
        hotel_service = HotelService(self.db)
        await hotel_service.get_hotel_or_raise(hotel_id)

        await self.get_room_or_raise(room_id)

        room_data_dumped = room_data.model_dump()
        room_data_ = RoomPatch(**room_data_dumped)
        await self.db.rooms.edit(room_data_, id=room_id, hotel_id=hotel_id)

        await self.db.rooms_to_facilities.update_facilities_in_room(
            room_id=room_id, facilities_ids=room_data_dumped["facilities_ids"]
        )

        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        hotel_service = HotelService(self.db)
        await hotel_service.get_hotel_or_raise(hotel_id)

        await self.get_room_or_raise(room_id)

        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()
