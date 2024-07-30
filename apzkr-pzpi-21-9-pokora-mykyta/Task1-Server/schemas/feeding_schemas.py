from pydantic import BaseModel, Field
from typing import Optional
from datetime import time


class FeedingScheduleBase(BaseModel):
    food_type: str = Field(..., description="Тип корму")
    scheduled_time: time = Field(..., description="Запланований час годування")


class FeedingScheduleCreate(FeedingScheduleBase):
    pass


class FeedingScheduleUpdate(BaseModel):
    food_type: Optional[str] = Field(None, description="Тип корму")
    scheduled_time: Optional[time] = Field(None, description="Запланований час годування")


class FeedingScheduleResponse(FeedingScheduleBase):
    id: int = Field(..., description="ID розкладу годування")
    aquarium_id: int = Field(..., description="ID акваріума")

    class Config:
        from_attributes = True
