from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete as sa_delete
from sqlalchemy import func, insert, select, update


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [
            self.schema.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True})) # Для дебага и получения сырого SQL запроса
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:
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
        if count > 1:
            raise HTTPException(status_code=422, detail="Найдено более одного объекта")
