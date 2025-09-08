from src.models.rooms import Rooms
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = Rooms
