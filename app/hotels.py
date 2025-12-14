from fastapi import Query, Body, APIRouter


router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]

@router.get("")
def get_hotels(
    id: int | None = Query(default=None, description="Айдишник"),
    title: str | None = Query(default=None, description="Название отеля"),
    name: str | None = Query(default=None, description="Имя отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        if name and hotel["name"] != name:
            continue

        hotels_.append(hotel)
    return hotels_

@router.delete("/{hotel_id}")
def delete_hotels(
        hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@router.post("")
def create_hotels(
    title: str = Body(embed=True),
    name: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    
    return {"status": "OK"}

@router.put("/{hotel_id}")
def update_hotels(
    hotel_id: int,
    title: str = Body(),
    name: str = Body(),
):
    global hotels
    
    hotel = [hotel for hotel in hotel if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    return {"status": "OK"}

@router.patch(
        path="/{hotel_id}",
        summary="Частичное обновление данных об отеле",
        description="<h1>Тут частично обновляются данные об отеле: можно отправить name, а можно title</h1>"
)
def edit_hotels(
    hotel_id: int,
    title: None | str = Body(default=None),
    name: None | str = Body(default=None),
):
    global hotels

    hotel = [hotel for hotel in hotel if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": "OK"}