from typing import Any, Sequence, Type

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete as sa_delete
from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base
from app.repositories.mappers.base import DataMapper


class BaseRepository:
    model: Type[Base]
    mapper: Type[DataMapper]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filter_by) -> list[BaseModel | Any]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs) -> list[BaseModel | Any]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by) -> BaseModel | None | Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> BaseModel | Any:
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True})) # Для дебага и получения сырого SQL запроса
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: Sequence[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True})) # Для дебага и получения сырого SQL запроса
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        await self._check_object_count(**filter_by)
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        await self._check_object_count(**filter_by)
        delete_stmt = sa_delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    async def _check_object_count(self, **filter_by):
        query = select(func.count()).select_from(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        count = result.scalar()
        if count == 0:
            raise HTTPException(status_code=404, detail="Объект не найден")
        if count > 1:  # type: ignore
            raise HTTPException(status_code=422, detail="Найдено более одного объекта")
