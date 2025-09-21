from src.models.bookings import Bookings
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = Bookings
    mapper = BookingDataMapper
