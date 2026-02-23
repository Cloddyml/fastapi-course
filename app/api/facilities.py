from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from app.api.dependencies import DBDep
from app.schemas.facilities import FacilityAdd
from app.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(
    db: DBDep,
):
    # print("Иду в БД")
    return await db.facilities.get_all()


@router.post("")
async def add_facilities(
    db: DBDep,
    facility_data: FacilityAdd = Body(
        openapi_examples={
            "1": {"summary": "Удобство 1", "value": {"title": "Интернет"}},
            "2": {"summary": "Удобство 2", "value": {"title": "Кондиционер"}},
        }
    ),
):
    facility = await FacilityService(db).create_facility(data=facility_data)
    return {"status": "OK", "data": facility}
