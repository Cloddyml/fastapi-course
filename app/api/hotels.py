from datetime import date

from fastapi import APIRouter, Body, Query

from app.api.dependencies import DBDep, PaginationDep
from app.schemas.hotels import HotelAdd, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Город отеля"),
    date_from: date = Query(example="2026-02-01"),
    date_to: date = Query(example="2026-02-10"),
):
    per_page = pagination.per_page or 5
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=(per_page * (pagination.page - 1)),
    # )
    return await db.hotels.get_filtered_by_time(
        location=location,
        title=title,
        limit=per_page,
        offset=(per_page * (pagination.page - 1)),
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{hotel_id}")
async def get_hotel(
    db: DBDep,
    hotel_id: int,
):
    return await db.hotels.get_one_or_none(
        id=hotel_id,
    )


@router.delete("/{hotel_id}")
async def delete_hotels(
    db: DBDep,
    hotel_id: int,
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotels(
    db: DBDep,
    hotel_data: HotelAdd = Body(
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotels(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelAdd,
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    path="/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут частично обновляются данные об отеле: можно отправить name, а можно title</h1>",
)
async def edit_hotels(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatch,
):
    await db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=True)
    await db.commit()
    return {"status": "OK"}
