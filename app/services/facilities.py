from app.schemas.facilities import FacilityAdd
from app.services.base import BaseService
from app.tasks.tasks import test_task


class FacilityService(BaseService):
    async def create_facility(self, data: FacilityAdd):
        facility = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()  # type: ignore
        return facility

    async def get_facilities(self):
        return await self.db.facilities.get_all()
