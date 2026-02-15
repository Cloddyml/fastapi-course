from app.models.rooms import RoomsOrm
from app.repositories.base import BaseRepository
from app.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room
