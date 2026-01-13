from fastapi import Body, Query, APIRouter
from sqlalchemy import insert, select, func

from app.api.dependencies import PaginationDep
from app.schemas.hotels import Hotel, HotelPatch
from app.database import async_session_maker, engine
from app.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Город отеля"),
    ):

    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            query = query.filter(func.lower(HotelsOrm.title).like(f"%{title.strip().lower()}%"))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).like(f"%{location.strip().lower()}%"))
        
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )

        # print(query.compile(engine, compile_kwargs={"literal_binds": True}))
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