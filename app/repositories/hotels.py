from app.repositories.base import BaseRepository
from app.models.hotels import HotelsOrm

class HotelsRepository(BaseRepository):
    model = HotelsOrm