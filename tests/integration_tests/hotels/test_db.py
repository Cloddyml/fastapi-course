from app.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Отель 5 звезд", location="Сочи")
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()
    print(f"{new_hotel_data=}")
