from datetime import date
from typing import Annotated

from fastapi import APIRouter, Body, Query

from app.api.dependencies import DBDep
from app.exceptions import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from app.schemas.rooms import RoomAddRequest, RoomPatchRequest
from app.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    date_from: Annotated[
        date,
        Query(
            ...,
            description="Start date (YYYY-MM-DD)",
            openapi_examples={"Дата 1": {"value": "2026-02-01"}},
        ),
    ],
    date_to: Annotated[
        date,
        Query(
            ...,
            description="End date (YYYY-MM-DD)",
            openapi_examples={"Дата 1": {"value": "2026-02-01"}},
        ),
    ],
    db: DBDep,
    hotel_id: int,
):
    return await RoomService(db).get_filtered_by_time(
        date_from=date_from, date_to=date_to, hotel_id=hotel_id
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        return await RoomService(db).get_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def create_rooms(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Комната 1",
                "value": {
                    "title": "VIP комната",
                    "description": "",
                    "price": 200,
                    "quantity": 3,
                    "facilities_ids": [1, 2],
                },
            },
            "2": {
                "summary": "Комната 2",
                "value": {
                    "title": "Рядовая комната",
                    "description": "",
                    "price": 100,
                    "quantity": 6,
                    "facilities_ids": [2, 1],
                },
            },
        }
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id=hotel_id, room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_rooms(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    await RoomService(db).update_rooms(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_rooms(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    await RoomService(db).edit_rooms(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_rooms(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    await RoomService(db).delete_rooms(hotel_id=hotel_id, room_id=room_id)
    return {"status": "OK"}
