from app.models.rooms import RoomsOrm
from app.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm
