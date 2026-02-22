from fastapi import APIRouter, Body, HTTPException

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import AllRoomsAreBookedException, ObjectNotFoundException
from app.schemas.bookings import BookingAdd, BookingAddRequest
from app.schemas.rooms import Room

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
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)  # type: ignore
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    # if not room:
    #     raise HTTPException(status_code=404, detail="Номер не найден")
    room_price: int = room.price

    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()

    return {"status": "OK", "data": booking}
