from fastapi import Body, Query, APIRouter

from schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get("")
def get_hotels(
    id: int | None = Query(default=None, de1scription="Айдишник"),
    title: str | None = Query(default=None, description="Название отеля"),
    name: str | None = Query(default=None, description="Имя отеля"),
    page: int | None = Query(default=1, description="Номер страницы с отелями"),
    per_page: int | None = Query(default=3, description="Количество отелей на одной странице"),
) -> list[Hotel]:
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        if name and hotel["name"] != name:
            continue

        hotels_.append(hotel)
    pagination = hotels_[per_page * (page - 1): per_page * page]
    return pagination

@router.delete("/{hotel_id}")
def delete_hotels(
        hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@router.post("")
def create_hotels(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi_u_morya"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай У фонтана",
        "name": "dubai_fountain"
    }},
    })):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    
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