from app.schemas.hotels import HotelAdd
from app.utils.db_manager import DBManager


async def test_add_hotel(db: DBManager):
    hotel_data = HotelAdd(title="Отель 5 звезд", location="Сочи")
    await db.hotels.add(hotel_data)
    await db.commit()
