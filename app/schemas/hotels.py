from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    name: str

class HotelPatch(BaseModel):
    title: str | None = Field(default=None)
    name: str | None = Field(default=None)