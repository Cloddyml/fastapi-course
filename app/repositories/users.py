from app.models.users import UsersOrm
from app.repositories.base import BaseRepository
from app.schemas.users import User


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User
