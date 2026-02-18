from pydantic import BaseModel, ConfigDict, Field


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = Field(default=None)
    price: int
    quantity: int
    facilities_ids: list[int] | None = None


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(default=None)
    price: int
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequest(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)
