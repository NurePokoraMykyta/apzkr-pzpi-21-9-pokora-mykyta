from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FeedingScheduleBase(BaseModel):
    food_type: str = Field(..., description="Тип корму")
    scheduled_time: datetime = Field(..., description="Запланований час годування")


class FeedingScheduleCreate(FeedingScheduleBase):
    pass


class FeedingScheduleUpdate(BaseModel):
    food_type: Optional[str] = Field(None, description="Тип корму")
    scheduled_time: Optional[datetime] = Field(None, description="Запланований час годування")


class FeedingScheduleResponse(FeedingScheduleBase):
    id: int = Field(..., description="ID розкладу годування")
    aquarium_id: int = Field(..., description="ID акваріума")

    class Config:
        from_attributes = True
