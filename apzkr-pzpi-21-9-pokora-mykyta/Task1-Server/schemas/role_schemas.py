from pydantic import BaseModel, Field
from typing import List, Optional


class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)


class RoleCreate(RoleBase):
    permissions: List[str] = Field(..., min_length=1)
    company_id: int = Field(...)


class RoleUpdate(RoleBase):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    permissions: Optional[List[str]] = Field(None, min_length=1)
    company_id: Optional[int] = Field(None)


class RoleFull(RoleBase):
    id: int
    permissions: List[str]
    company_id: int

    class Config:
        from_attributes = True


class RoleResponse(RoleFull):
    pass
