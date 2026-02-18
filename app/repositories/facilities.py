from app.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from app.repositories.base import BaseRepository
from app.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility
