from fastapi import APIRouter, Body, Query

from app.database import async_session_maker
from app.repositories.rooms import RoomsRepository
from app.schemas.rooms import RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])


@router.get("")
async def get_rooms(
    hotel_id: int,
    title: str | None = Query(default=None, description="Заголовок комнаты"),
    description: str | None = Query(default=None, description="Описание комнаты"),
    price: int | None = Query(default=None, description="Цена комнаты"),
    quantity: int | None = Query(default=None, description="Количество комнат"),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            description=description,
            price=price,
            quantity=quantity,
        )


@router.get("/{room_id}")
async def get_room(
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            hotel_id=hotel_id,
            id=room_id,
        )


@router.delete("/{room_id}")
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


@router.post("")
async def create_rooms(
    hotel_id: int,
    room_data: RoomAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Комната 1",
                "value": {
                    "title": "VIP комната",
                    "description": "",
                    "price": 200,
                    "quantity": 3,
                },
            },
            "2": {
                "summary": "Комната 2",
                "value": {
                    "title": "Рядовая комната",
                    "description": "",
                    "price": 100,
                    "quantity": 6,
                },
            },
        }
    ),
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data, hotel_id=hotel_id)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{room_id}")
async def update_rooms(
    hotel_id: int,
    room_id: int,
    room_data: RoomAdd,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{room_id}")
async def edit_rooms(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatch,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True
        )
        await session.commit()
    return {"status": "OK"}
