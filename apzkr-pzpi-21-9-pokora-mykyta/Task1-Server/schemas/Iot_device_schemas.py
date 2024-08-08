from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class IoTDeviceBase(BaseModel):
    unique_address: str = Field(..., description="Унікальна адреса IoT пристрою")


class IoTDeviceCreate(IoTDeviceBase):
    pass


class IoTDeviceUpdate(BaseModel):
    unique_address: Optional[str] = Field(None, description="Унікальна адреса IoT пристрою")


class IoTDeviceResponse(IoTDeviceBase):
    id: int = Field(..., description="ID IoT пристрою")
    aquarium_id: int = Field(..., description="ID акваріума")
    is_active: bool = Field(..., description="Статус активності пристрою")

    class Config:
        from_attributes = True
