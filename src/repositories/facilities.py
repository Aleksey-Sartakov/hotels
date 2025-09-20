from src.models.facilities import Facilities
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility


class FacilitiesRepository(BaseRepository):
    model = Facilities
    schema = Facility
