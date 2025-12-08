from fastapi import APIRouter, Body
from fastapi.openapi.models import Example
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, RedisDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService

facilities_router = APIRouter(prefix="/facilities", tags=["Удобства"])


@facilities_router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep, redis: RedisDep):
    facility_service = FacilityService(db)
    facilities = await facility_service.get_facilities()

    return facilities


@facilities_router.delete("")
async def delete_facilities(facility_id: int, db: DBDep):
    facility_service = FacilityService(db)
    await facility_service.delete_facility(facility_id)

    return {"status": "No content"}


@facilities_router.post("")
async def create_facilities(
    db: DBDep,
    facility_add: FacilityAdd = Body(
        openapi_examples={
            "1": Example(summary="Кондиционер", value={"title": "Кондиционер"}),
            "2": Example(summary="Душ", value={"title": "Душ"}),
            "3": Example(summary="Телевизор", value={"title": "Телевизор"}),
        }
    ),
):
    facility_service = FacilityService(db)
    facility = await facility_service.create_facility(facility_add)

    return {"status": "Created", "data": facility}
