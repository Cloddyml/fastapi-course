from fastapi import APIRouter

from app.database import async_session_maker
from app.repositories.users import UsersRepository
from app.schemas.users import UserAdd, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = "1234234esdftgdgh43r3"
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}
