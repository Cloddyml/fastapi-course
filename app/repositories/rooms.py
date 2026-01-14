from app.repositories.base import BaseRepository
from app.models.rooms import RoomsOrm

class RoomsRepository(BaseRepository):
    model = RoomsOrm