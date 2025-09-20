from typing import Iterable

from sqlalchemy import delete, select

from src.models.facilities import Facilities, RoomsToFacilities
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomToFacility, RoomToFacilityAdd


class FacilitiesRepository(BaseRepository):
    model = Facilities
    schema = Facility


class RoomsToFacilitiesRepository(BaseRepository):
    model = RoomsToFacilities
    schema = RoomToFacility

    async def update_facilities_in_room(self, room_id: int, facilities_ids: list[int] | None = None):
        if not facilities_ids:
            await self.delete_facilities_from_room(room_id=room_id)
        else:
            current_facilities_ids_query = (
                select(RoomsToFacilities.facility_id)
                .filter_by(room_id=room_id)
            )
            current_facilities_ids = await self.session.execute(current_facilities_ids_query)
            current_facilities_ids = set(current_facilities_ids.scalars().all())

            facilities_to_delete = current_facilities_ids - set(facilities_ids)
            if facilities_to_delete:
                await self.delete_facilities_from_room(room_id=room_id, facilities_ids=facilities_to_delete)

            facilities_to_add = set(facilities_ids) - current_facilities_ids
            if facilities_to_add:
                await self.add_bulk(
                    [RoomToFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in facilities_to_add]
                )

    async def delete_facilities_from_room(self, room_id: int, facilities_ids: Iterable[int] | None = None):
        stmt = delete(self.model).filter_by(room_id=room_id)
        if facilities_ids:
            stmt = stmt.filter(RoomsToFacilities.facility_id.in_(facilities_ids))

        await self.session.execute(stmt)
