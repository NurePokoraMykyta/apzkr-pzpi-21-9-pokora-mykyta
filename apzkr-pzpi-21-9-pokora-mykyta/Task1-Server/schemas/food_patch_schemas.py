from pydantic import BaseModel, Field


class FoodPatchBase(BaseModel):
    name: str = Field(..., description="Назва порції корму")
    food_type: str = Field(..., description="Тип корму")
    quantity: float = Field(..., gt=0, description="Кількість корму в грамах")


class FoodPatchCreate(FoodPatchBase):
    pass


class FoodPatchResponse(FoodPatchBase):
    id: int = Field(..., description="ID порції корму")
    iot_device_id: int = Field(..., description="ID IoT пристрою")

    class Config:
        from_attributes = True
