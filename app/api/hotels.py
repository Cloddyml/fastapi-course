from fastapi import Body, Query, APIRouter
from sqlalchemy import insert, select

from app.api.dependencies import PaginationDep
from app.schemas.hotels import Hotel, HotelPatch
from app.database import async_session_maker, engine
from app.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(default=None, de1scription="Айдишник"),
    title: str | None = Query(default=None, description="Название отеля"),
    name: str | None = Query(default=None, description="Имя отеля"),
    ) -> list[Hotel]:

    async with async_session_maker() as session:
        query = select(HotelsOrm)
        result = await session.execute(query)

        # print(type(result), result)
        hotels = result.scalars().all()
        # print(type(hotels), hotels)
        return hotels
    
    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]

@router.delete("/{hotel_id}")
def delete_hotels(
        hotel_id: int,
    ):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@router.post("")
async def create_hotels(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель 5 звезд у моря",
        "location": "Сочи"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель У фонтана",
        "location": "Дубай"
    }},
    })):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True})) # Для дебага и получения сырого SQL запроса
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}

@router.put("/{hotel_id}")
def update_hotels(hotel_id: int, hotel_data: Hotel,):

    global hotels
    
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}

@router.patch(
        path="/{hotel_id}",
        summary="Частичное обновление данных об отеле",
        description="<h1>Тут частично обновляются данные об отеле: можно отправить name, а можно title</h1>"
)
def edit_hotels(hotel_id: int, hotel_data: HotelPatch,):
    global hotels

    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}