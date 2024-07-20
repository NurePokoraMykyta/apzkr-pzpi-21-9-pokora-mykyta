from fastapi import APIRouter, Depends, HTTPException
from typing import List

from schemas.role_schemas import RoleCreate, RoleUpdate, RoleResponse
from services.role_manager import RoleManager, get_role_manager, require_permissions
from api.user import get_current_user

role_router = APIRouter(tags=["Ролі"], prefix="/roles")


@role_router.post("", response_model=RoleResponse)
@require_permissions("manage_roles")
async def create_role(
        role_data: RoleCreate,
        current_user: dict = Depends(get_current_user),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        new_role = role_manager.create_role(
            role_data.name,
            role_data.description,
            role_data.permissions,
            role_data.company_id
        )
        return RoleResponse.from_orm(new_role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@role_router.get("/company/{company_id}", response_model=List[RoleResponse])
@require_permissions("view_company")
async def get_company_roles(
        company_id: int,
        current_user: dict = Depends(get_current_user),
        role_manager: RoleManager = Depends(get_role_manager)
):
    if not role_manager.has_company_access(current_user['uid'], company_id):
        raise HTTPException(status_code=403, detail="Немає доступу до цієї компанії")
    roles = role_manager.get_company_roles(company_id)
    return list(roles)


@role_router.get("/company/{company_id}/role/{role_id}", response_model=RoleResponse)
@require_permissions("view_company")
async def get_company_role(
        company_id: int,
        role_id: int,
        current_user: dict = Depends(get_current_user),
        role_manager: RoleManager = Depends(get_role_manager)
):
    if not role_manager.has_company_access(current_user['uid'], company_id):
        raise HTTPException(status_code=403, detail="Немає доступу до цієї компанії")
    try:
        role = role_manager.get_company_role(company_id, role_id)
        return role
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@role_router.put("/{role_id}", response_model=RoleResponse)
@require_permissions("manage_roles")
async def update_role(
        role_id: int,
        role_data: RoleUpdate,
        current_user: dict = Depends(get_current_user),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        updated_role = role_manager.update_role_permissions(role_id, role_data.permissions)
        return updated_role
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@role_router.post("/{role_id}/assign")
@require_permissions("manage_roles")
async def assign_role_to_user(
        role_id: int,
        user_uid: str,
        company_id: int,
        current_user: dict = Depends(get_current_user),
        role_manager: RoleManager = Depends(get_role_manager)
):
    if not role_manager.has_company_access(current_user['uid'], company_id):
        raise HTTPException(status_code=403, detail="Немає доступу до цієї компанії")
    try:
        role_manager.assign_role(user_uid, role_id, company_id)
        return {"message": "Роль успішно призначено користувачу"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
