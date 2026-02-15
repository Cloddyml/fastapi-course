from fastapi import APIRouter, Body

from app.api.dependencies import DBDep, UserIdDep
from app.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(
    db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_filtered(
        user_id=user_id,
    )


@router.post("")
async def add_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Бронирование 1",
                "value": {
                    "room_id": 3,
                    "date_from": "2026-02-15",
                    "date_to": "2026-02-17",
                },
            },
            "2": {
                "summary": "Бронирование 2",
                "value": {
                    "room_id": 4,
                    "date_from": "2026-02-15",
                    "date_to": "2026-02-15",
                },
            },
        }
    ),
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price

    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}
