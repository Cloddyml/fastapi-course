from sqlalchemy import func, select

from app.models.hotels import HotelsOrm
from app.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsOrm)
        if title:
            query = query.filter(
                func.lower(HotelsOrm.title).contains(title.strip().lower())
            )
        if location:
            query = query.filter(
                func.lower(HotelsOrm.location).contains(location.strip().lower())
            )

        query = query.limit(limit).offset(offset)

        # print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return result.scalars().all()

        # print(type(result), result)
        # print(type(hotels), hotels)

        # if pagination.page and pagination.per_page:
        # return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
