from src.models.bookings import Bookings
from src.models.facilities import Facilities, RoomsToFacilities
from src.models.hotels import Hotels
from src.models.rooms import Rooms
from src.models.users import Users
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility, RoomToFacility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = Hotels
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = Rooms
    schema = Room


class RoomWithRelsDataMapper(DataMapper):
    db_model = Rooms
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = Users
    schema = User


class BookingDataMapper(DataMapper):
    db_model = Bookings
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = Facilities
    schema = Facility


class RoomToFacilityDataMapper(DataMapper):
    db_model = RoomsToFacilities
    schema = RoomToFacility
