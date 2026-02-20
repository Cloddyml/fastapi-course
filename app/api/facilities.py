import json

from fastapi import APIRouter, Body

from app import redis_manager
from app.api.dependencies import DBDep
from app.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(
    db: DBDep,
):
    facilities_from_cache = await redis_manager.get("facilities")
    # print(f"{facilities_from_cache=}")
    if not facilities_from_cache:
        print("Иду в БД")
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, 10)
        return facilities
    else:
        facilities_dic = json.loads(facilities_from_cache)
        return facilities_dic


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
