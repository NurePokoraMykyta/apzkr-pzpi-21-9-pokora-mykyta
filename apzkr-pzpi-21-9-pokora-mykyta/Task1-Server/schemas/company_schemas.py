from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CompanyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Назва компанії")
    description: Optional[str] = Field(None, max_length=500, description="Опис компанії")


class CompanyUpdate(CompanyCreate):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Назва компанії")


class CompanyFull(CompanyCreate):
    id: int = Field(..., description="ID компанії")
    created_at: datetime = Field(..., description="Дата створення")
    updated_at: datetime = Field(..., description="Дата оновлення")

    class Config:
        from_attributes = True


class CompanyResponse(CompanyFull):
    pass