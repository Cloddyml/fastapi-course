from app.models.bookings import BookingsOrm
from app.repositories.base import BaseRepository
from app.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
