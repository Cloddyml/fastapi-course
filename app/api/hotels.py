from datetime import date
from typing import Annotated

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from app.api.dependencies import DBDep, PaginationDep
from app.exceptions import (
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
)
from app.schemas.hotels import HotelAdd, HotelPatch
from app.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
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
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Город отеля"),
):
    await HotelService(db).get_filtered_by_time(
        date_from,  # type: ignore
        date_to,  # type: ignore
        pagination,
        title,
        location,
    )


@router.get("/{hotel_id}")
async def get_hotel(
    db: DBDep,
    hotel_id: int,
):
    try:
        return await HotelService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


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
    hotel = await HotelService(db).add_hotel(data=hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotels(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelAdd,
):
    await HotelService(db).update_hotels(data=hotel_data, hotel_id=hotel_id)
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
    await HotelService(db).edit_hotels(data=hotel_data, hotel_id=hotel_id)
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotels(
    db: DBDep,
    hotel_id: int,
):
    await HotelService(db).delete_hotels(hotel_id=hotel_id)
    return {"status": "OK"}
