from datetime import date

from src.schemas.bookings import BookingAdd, BookingUpdate


async def test_booking_crud(db):
    user = (await db.users.get_all())[0]
    room = (await db.rooms.get_all())[0]

    # добавить бронь
    booking_data = BookingAdd(
        date_from=date(year=2026, month=1, day=1),
        date_to=date(year=2026, month=1, day=10),
        room_id=room.id,
        user_id=user.id,
        price=100
    )
    created_booking = await db.bookings.add(booking_data)

    assert created_booking.date_from == date(year=2026, month=1, day=1)
    assert created_booking.date_to == date(year=2026, month=1, day=10)
    assert created_booking.room_id == room.id
    assert created_booking.user_id == user.id
    assert created_booking.price == 100

    # обновить бронь
    await db.bookings.edit(BookingUpdate(price=200, date_from=date(year=2026, month=1, day=5)), exclude_unset=True)
    created_booking = await db.bookings.get_one_or_none(id=created_booking.id)
    assert created_booking.price == 200
    assert created_booking.date_from == date(year=2026, month=1, day=5)

    # удалить бронь
    all_bookings_len_before = len(await db.bookings.get_all())
    await db.bookings.delete(id=created_booking.id)
    all_bookings_len_after = len(await db.bookings.get_all())
    assert all_bookings_len_before == all_bookings_len_after + 1
