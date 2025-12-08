from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def create_facility(self, facility_add: FacilityAdd):
        facility = await self.db.facilities.add(facility_add)
        await self.db.commit()

        test_task.delay()

        return facility

    async def get_facilities(self):
        facilities = await self.db.facilities.get_all()

        return facilities

    async def delete_facility(self, facility_id: int):
        await self.db.facilities.delete(id=facility_id)
        await self.db.commit()
