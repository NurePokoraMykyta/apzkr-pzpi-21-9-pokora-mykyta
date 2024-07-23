from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class WaterParameterBase(BaseModel):
    ph: float = Field(..., description="Рівень pH")
    temperature: float = Field(..., description="Температура води")
    salinity: float = Field(..., description="Рівень солоності")
    oxygen_level: float = Field(..., description="Рівень кисню")
    measured_at: datetime = Field(..., description="Час вимірювання")


class WaterParameterCreate(WaterParameterBase):
    aquarium_id: int = Field(..., description="ID акваріума")


class WaterParameterUpdate(BaseModel):
    ph: Optional[float] = Field(None, description="Рівень pH")
    temperature: Optional[float] = Field(None, description="Температура води")
    salinity: Optional[float] = Field(None, description="Рівень солоності")
    oxygen_level: Optional[float] = Field(None, description="Рівень кисню")
    measured_at: Optional[datetime] = Field(None, description="Час вимірювання")


class WaterParameterResponse(WaterParameterBase):
    id: int = Field(..., description="ID параметра води")
    aquarium_id: int = Field(..., description="ID акваріума")

    class Config:
        from_attributes = True
