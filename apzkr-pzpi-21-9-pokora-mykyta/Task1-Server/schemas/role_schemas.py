from pydantic import BaseModel, Field
from typing import List, Optional


class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Назва ролі")
    description: Optional[str] = Field(None, max_length=200, description="Опис ролі")


class RoleCreate(RoleBase):
    permissions: List[str] = Field(..., min_length=1, description="Дозволи")
    company_id: int = Field(..., description="ID компанії")


class RoleUpdate(RoleBase):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Назва ролі")
    permissions: Optional[List[str]] = Field(None, min_length=1, description="Дозволи")
    company_id: Optional[int] = Field(None, description="ID компанії")


class RoleFull(RoleBase):
    id: int = Field(..., description="ID ролі")
    permissions: List[str] = Field(..., description="Дозволи")

    class Config:
        from_attributes = True


class RoleResponse(RoleFull):
    pass