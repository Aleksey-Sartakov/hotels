from fastapi import APIRouter, Body, HTTPException, status
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException, \
    DateToLessOrEqualThenDateFromException, BookingDateToLessOrEqualThenDateFromHTTPException, \
    DateCannotBeInPastException, DateCannotBeInPastHTTPException
from src.schemas.bookings import BookingAddRequest, BookingAdd


bookings_router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@bookings_router.get("")
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()

    return bookings


@bookings_router.get("/me")
async def get_self_bookings(db: DBDep, user_id: UserIdDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)

    return bookings


@bookings_router.delete("")
async def delete_bookings(booking_id: int, db: DBDep):
    await db.bookings.delete(id=booking_id)
    await db.commit()

    return {"status": "No content"}


@bookings_router.post("")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAddRequest = Body(
        openapi_examples={
            "1": Example(
                summary="Бронирование 1", value={"date_from": "2026-01-01", "date_to": "2026-01-10", "room_id": 2}
            ),
            "2": Example(
                summary="Бронирование 2", value={"date_from": "2026-01-01", "date_to": "2026-01-03", "room_id": 3}
            )
        }
    ),
):
    try:
        room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump(exclude_unset=True))
    try:
        booking = await db.bookings.add_booking(_booking_data)

    except AllRoomsAreBookedException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Не осталось свободных номеров.")

    except DateToLessOrEqualThenDateFromException:
        raise BookingDateToLessOrEqualThenDateFromHTTPException

    except DateCannotBeInPastException:
        raise DateCannotBeInPastHTTPException

    await db.commit()

    return {"status": "Created", "data": booking}
