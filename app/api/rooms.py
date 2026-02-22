from datetime import date
from typing import Annotated

from fastapi import APIRouter, Body, Query

from app.api.dependencies import DBDep
from app.exceptions import (
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
    RoomNotFoundHTTPException,
    check_date_to_after_date_from,
)
from app.schemas.facilities import RoomFacilityAdd
from app.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: Annotated[
        date | None,
        Query(
            openapi_examples={
                "Дата 1": {"value": "2026-02-01"},
            }
        ),
    ] = None,
    date_to: Annotated[
        date | None,
        Query(
            openapi_examples={
                "Дата 1": {"value": "2026-02-01"},
            }
        ),
    ] = None,
):
    check_date_to_after_date_from(date_from=date_from, date_to=date_to)
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    room = await db.rooms.get_one_or_none_with_rels(
        id=room_id,
        hotel_id=hotel_id,
    )
    if not room:
        raise HotelNotFoundHTTPException
    return room


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_rooms(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    await db.rooms.delete(
        id=room_id,
        hotel_id=hotel_id,
    )
    await db.commit()
    return {"status": "OK"}


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
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)  # type: ignore
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_rooms(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities_ids=room_data.facilities_ids
    )
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_rooms(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(
        _room_data,
        id=room_id,
        hotel_id=hotel_id,
        exclude_unset=True,
    )
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"status": "OK"}
