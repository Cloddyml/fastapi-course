from app.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Отель 5 звезд", location="Сочи")
    await db.hotels.add(hotel_data)
    await db.commit()
