from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

from schemas.role_schemas import RoleResponse


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


class UserCompanyResponse(BaseModel):
    id: int = Field(..., description="ID користувача")
    email: EmailStr = Field(..., description="Електронна пошта користувача")
    display_name: Optional[str] = Field(None, description="Ім'я користувача для відображення")
    phone_number: Optional[str] = Field(None, description="Номер телефону користувача")
    status: str = Field(..., description="Статус користувача")
    created_at: datetime = Field(..., description="Дата створення")
    updated_at: Optional[datetime] = Field(None, description="Дата оновлення")
    role: Optional[RoleResponse] = Field(None, description="Роль користувача в компанії")

    class Config:
        from_attributes = True
