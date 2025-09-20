from sqlalchemy import delete

from src.models.facilities import Facilities, RoomsToFacilities
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomToFacility


class FacilitiesRepository(BaseRepository):
    model = Facilities
    schema = Facility


class RoomsToFacilitiesRepository(BaseRepository):
    model = RoomsToFacilities
    schema = RoomToFacility

    async def delete_facilities(self, room_id: int, facilities_ids: list[int] | None = None):
        stmt = delete(self.model).filter_by(room_id=room_id)
        if facilities_ids:
            stmt = stmt.filter(RoomsToFacilities.facility_id.in_(facilities_ids))

        await self.session.execute(stmt)
