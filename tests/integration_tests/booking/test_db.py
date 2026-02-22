from datetime import date

from app.schemas.bookings import Booking, BookingAdd
from app.utils.db_manager import DBManager


async def test_booking_crud(db: DBManager):
    user_id = (await db.users.get_all())[0].id  # type: ignore
    room_id = (await db.rooms.get_all())[0].id  # type: ignore
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=12, day=12),
        date_to=date(year=2026, month=1, day=1),
        price=100,
    )
    # CREATE AND READ
    new_booking: Booking = await db.bookings.add(booking_data)  # type: ignore
    booking: Booking | None = await db.bookings.get_one_or_none(id=new_booking.id)  # type: ignore
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    # UPDATE
    new_date_from = date(year=2026, month=12, day=12)
    new_date_to = date(year=2027, month=1, day=1)
    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=new_date_from,
        date_to=new_date_to,
        price=100,
    )
    await db.bookings.edit(update_booking_data, id=new_booking.id)
    updated_booking: Booking | None = await db.bookings.get_one_or_none(id=new_booking.id)  # type: ignore
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_from == new_date_from
    assert updated_booking.date_to == new_date_to

    # DELETE
    await db.bookings.delete(id=updated_booking.id)
    deleted_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not deleted_booking
