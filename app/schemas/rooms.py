from pydantic import BaseModel, ConfigDict, Field

from app.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = Field(default=None)
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(default=None)
    price: int
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatchRequest(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)
    facilities_ids: list[int] = []


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)
