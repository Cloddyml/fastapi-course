from datetime import date

from app.api.dependencies import PaginationDep
from app.exceptions import check_date_to_after_date_from
from app.schemas.hotels import HotelAdd, HotelPatch
from app.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        pagination: PaginationDep,
        title: str | None,
        location: str | None,
    ):
        check_date_to_after_date_from(date_from=date_from, date_to=date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            location=location,
            title=title,
            limit=per_page,
            offset=(per_page * (pagination.page - 1)),
            date_from=date_from,
            date_to=date_to,
        )
        # return {"status": "OK", "data": hotels}

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(
        self,
        data: HotelAdd,
    ):

        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def update_hotels(
        self,
        hotel_id: int,
        data: HotelAdd,
    ):
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()

    async def edit_hotels(
        self,
        hotel_id: int,
        data: HotelPatch,
    ):
        await self.db.hotels.edit(data, id=hotel_id, exclude_unset=True)
        await self.db.commit()

    async def delete_hotels(
        self,
        hotel_id: int,
    ):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
