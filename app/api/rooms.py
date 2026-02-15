from fastapi import APIRouter, Body

from app.database import async_session_maker
from app.repositories.rooms import RoomsRepository
from app.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            id=room_id,
            hotel_id=hotel_id,
        )


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_rooms(
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(
            id=room_id,
            hotel_id=hotel_id,
        )
        await session.commit()
    return {"status": "OK"}


@router.post("/{hotel_id}/rooms")
async def create_rooms(
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Комната 1",
                "value": {
                    "hotel_id": 1,
                    "title": "VIP комната",
                    "description": "",
                    "price": 200,
                    "quantity": 3,
                },
            },
            "2": {
                "summary": "Комната 2",
                "value": {
                    "hotel_id": 1,
                    "title": "Рядовая комната",
                    "description": "",
                    "price": 100,
                    "quantity": 6,
                },
            },
        }
    ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_rooms(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_rooms(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            _room_data,
            id=room_id,
            hotel_id=hotel_id,
            exclude_unset=True,
        )
        await session.commit()
    return {"status": "OK"}
