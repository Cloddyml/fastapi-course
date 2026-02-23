from typing import Annotated

from fastapi import Depends, Query, Request
from pydantic import BaseModel

from app.database import async_session_maker
from app.exceptions import (
    IncorrectTokenException,
    IncorrectTokenHTTPException,
    NoAccessTokenHTTPException,
)
from app.services.auth import AuthService
from app.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int, Query(default=1, description="Номер страницы с отелями", ge=1)]
    per_page: Annotated[
        int | None,
        Query(default=None, description="Количество отелей на одной странице", ge=1, lt=30),
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise NoAccessTokenHTTPException
    return access_token


def get_current_user_id(access_token: str = Depends(get_token)) -> int:
    try:
        data = AuthService().decode_token(access_token)
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
