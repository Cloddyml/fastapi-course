from app.models.hotels import HotelsOrm
from app.repositories.mappers.base import DataMapper
from app.schemas.hotels import Hotel


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel
