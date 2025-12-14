from fastapi import FastAPI, Query, Body
import uvicorn


app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]

@app.get("/hotels")
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

@app.delete("/hotels/{hotel_id}")
def delete_hotels(
        hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@app.post("/hotels")
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

@app.put("/hotels/{hotel_id}")
def update_hotels(
    hotel_id: int,
    title: str = Body(embed=True),
    name: str = Body(embed=True),
):
    global hotels
    
    for hotel in hotels:
        if hotel["id"] != hotel_id:
            continue
        else:
            hotel["title"] = title
            hotel["name"] = name
            
            return {"status": "OK"}
    return {"status": "NOT OK"}

@app.patch("/hotels/{hotel_id}")
def edit_hotels(
    hotel_id: int,
    title: None | str = Body(default=None, embed=True),
    name: None | str = Body(default=None, embed=True),
):
    global hotels

    if name == None and title == None:
        return {"status": "NOT OK"}
    else:
        if name != None and title == None:
            hotels[hotel_id - 1]["name"] = name
        elif title != None and name == None:
            hotels[hotel_id - 1]["title"] = title
        else:
            return {"status": "NOT OK"}

    return {"status": "OK"}

def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
