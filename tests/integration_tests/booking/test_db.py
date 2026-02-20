from datetime import date

from app.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=12, day=12),
        date_to=date(year=2026, month=1, day=1),
        price=100,
    )
    # CREATE AND READ
    new_booking = await db.bookings.add(booking_data)
    check_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert check_booking
    assert check_booking.id == new_booking.id

    # UPDATE
    new_date_from = date(year=2026, month=12, day=12)
    new_date_to = date(year=2027, month=1, day=1)
    booking_update_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=new_date_from,
        date_to=new_date_to,
        price=100,
    )
    await db.bookings.edit(booking_update_data)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.date_from == new_date_from
    assert updated_booking.date_to == new_date_to

    # DELETE
    await db.bookings.delete(id=updated_booking.id)
    deleted_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not deleted_booking
    await db.commit()
