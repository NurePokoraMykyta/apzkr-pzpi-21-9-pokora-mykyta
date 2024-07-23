from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from schemas.company_schemas import CompanyResponse
from schemas.feeding_schemas import FeedingScheduleResponse
from schemas.fish_schemas import FishResponse
from schemas.water_parameter_schemas import WaterParameterResponse


class AquariumBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Назва акваріуму")
    capacity: float = Field(..., gt=0, description="Об'єм акваріуму в літрах")
    description: Optional[str] = Field(None, max_length=500, description="Опис акваріуму")


class AquariumCreate(AquariumBase):
    pass


class AquariumUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Назва акваріуму")
    capacity: Optional[float] = Field(None, gt=0, description="Об'єм акваріуму в літрах")
    description: Optional[str] = Field(None, max_length=500, description="Опис акваріуму")


class AquariumFull(AquariumBase):
    id: int = Field(..., description="ID акваріуму")
    created_at: datetime = Field(..., description="Дата створення")
    updated_at: Optional[datetime] = Field(None, description="Дата оновлення")
    company: CompanyResponse
    feeding_schedules: List[FeedingScheduleResponse] = []
    water_parameters: List[WaterParameterResponse] = []
    fish: List[FishResponse] = []
    #iot_device: Optional[IoTDeviceResponse] = None

    class Config:
        from_attributes = True


class AquariumResponse(AquariumFull):
    pass