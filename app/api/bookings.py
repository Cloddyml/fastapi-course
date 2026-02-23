from fastapi import APIRouter, Body

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from app.schemas.bookings import BookingAddRequest
from app.services.booking import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(
    db: DBDep,
):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await BookingService(db).get_my_bookings(user_id)


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
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}
