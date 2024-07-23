from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FishBase(BaseModel):
    species: str = Field(..., description="Вид риби")
    quantity: int = Field(..., description="Кількість риб")


class FishCreate(FishBase):
    aquarium_id: int = Field(..., description="ID акваріума")


class FishUpdate(BaseModel):
    species: Optional[str] = Field(None, description="Вид риби")
    quantity: Optional[int] = Field(None, description="Кількість риб")


class FishResponse(FishBase):
    id: int = Field(..., description="ID запису про рибу")
    aquarium_id: int = Field(..., description="ID акваріума")

    class Config:
        from_attributes = True
