from fastapi import APIRouter, Body

from app.api.dependencies import DBDep
from app.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(
    db: DBDep,
):
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
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}
