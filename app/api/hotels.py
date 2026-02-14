from fastapi import APIRouter, Body, Query

from app.api.dependencies import PaginationDep
from app.database import async_session_maker
from app.repositories.hotels import HotelsRepository
from app.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Город отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=(per_page * (pagination.page - 1)),
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int): ...


@router.delete("/{hotel_id}")
async def delete_hotels(
    hotel_id: int,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotels(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Отель 5 звезд у моря", "location": "Сочи"},
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Отель У фонтана", "location": "Дубай"},
            },
        }
    ),
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotels(
    hotel_id: int,
    hotel_data: Hotel,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    path="/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут частично обновляются данные об отеле: можно отправить name, а можно title</h1>",
)
async def edit_hotels(
    hotel_id: int,
    hotel_data: HotelPatch,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            hotel_data, id=hotel_id, exclude_unset=True
        )
        await session.commit()
    return {"status": "OK"}
