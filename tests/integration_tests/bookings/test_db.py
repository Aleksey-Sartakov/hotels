from datetime import date

from src.schemas.bookings import BookingAdd, BookingUpdate


async def test_booking_crud(db):
    user = (await db.users.get_all())[0]
    room = (await db.rooms.get_all())[0]

    booking_data = BookingAdd(
        date_from=date(year=2026, month=1, day=1),
        date_to=date(year=2026, month=1, day=10),
        room_id=room.id,
        user_id=user.id,
        price=100
    )
    await db.bookings.add(booking_data)
    await db.commit()

    all_bookings = await db.bookings.get_all()
    assert len(all_bookings) == 1

    created_booking = all_bookings[0]
    assert created_booking.date_from == date(year=2026, month=1, day=1)
    assert created_booking.date_to == date(year=2026, month=1, day=10)
    assert created_booking.room_id == room.id
    assert created_booking.user_id == user.id
    assert created_booking.price == 100

    await db.bookings.edit(BookingUpdate(price=200, date_from=date(year=2026, month=1, day=5)), exclude_unset=True)
    await db.commit()
    created_booking = await db.bookings.get_one_or_none(id=created_booking.id)
    assert created_booking.price == 200
    assert created_booking.date_from == date(year=2026, month=1, day=5)

    await db.bookings.delete(id=created_booking.id)
    await db.commit()
    all_bookings = await db.bookings.get_all()
    assert len(all_bookings) == 0
