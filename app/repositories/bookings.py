from app.models.bookings import BookingsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper
