from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CompanyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CompanyUpdate(CompanyCreate):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class CompanyFull(CompanyCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CompanyResponse(CompanyFull):
    pass
