from fastapi import APIRouter, Depends, HTTPException
from typing import List

from data import Company, db_session
from schemas.company_schemas import CompanyCreate, CompanyUpdate, CompanyResponse
from services.user_service import user_service
from services.company_service import CompanyService, get_company_manager
from services.role_manager import require_permissions, RoleManager, get_role_manager
from api.user import get_current_user
from sqlalchemy.orm import Session

company_router = APIRouter(tags=["Компанії"], prefix="/companies")


@company_router.post("", response_model=CompanyResponse)
@require_permissions("create_company")
async def create_company(
        company_data: CompanyCreate,
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
):
    try:
        new_company = company_service.create_company(company_data, current_user['uid'])
        return CompanyResponse.from_orm(new_company)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@company_router.get("", response_model=List[CompanyResponse])
@require_permissions("view_companies")
async def get_companies(
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager)
):
    companies = company_service.get_companies()
    return [CompanyResponse.from_orm(company) for company in companies]


@company_router.get("/{company_id}", response_model=CompanyResponse)
@require_permissions("view_company")
async def get_company(
        company_id: int,
        company_service: CompanyService = Depends(get_company_manager)
):
    try:
        company = company_service.get_company(company_id)
        return CompanyResponse.from_orm(company)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@company_router.put("/{company_id}", response_model=CompanyResponse)
@require_permissions("edit_company")
async def update_company(
        company_id: int,
        company_data: CompanyUpdate,
        company_service: CompanyService = Depends(get_company_manager)
):
    try:
        updated_company = company_service.update_company(company_id, company_data)
        return CompanyResponse.from_orm(updated_company)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@company_router.delete("/{company_id}")
@require_permissions("delete_company")
async def delete_company(
        company_id: int,
        company_service: CompanyService = Depends(get_company_manager)
):
    try:
        return company_service.delete_company(company_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@company_router.post("/{company_id}/users")
@require_permissions("manage_users")
async def add_user_to_company(
        company_id: int,
        user_uid: str,
        role_id: int,
        company_service: CompanyService = Depends(get_company_manager)
):
    try:
        return company_service.add_user_to_company(company_id, user_uid, role_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@company_router.delete("/{company_id}/users/{user_uid}")
@require_permissions("manage_users")
async def remove_user_from_company(
        company_id: int,
        user_uid: str,
        company_service: CompanyService = Depends(get_company_manager)
):
    try:
        return company_service.remove_user_from_company(company_id, user_uid)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
