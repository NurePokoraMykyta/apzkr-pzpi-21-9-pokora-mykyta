from functools import wraps

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Annotated

from data import Company, db_session
from schemas.aquarium_schemas import AquariumResponse, AquariumCreate
from schemas.company_schemas import CompanyCreate, CompanyUpdate, CompanyResponse
from services.user_service import user_service
from services.company_service import CompanyService, get_company_manager
from services.role_manager import RoleManager, get_role_manager
from api.user import get_current_user
from sqlalchemy.orm import Session
import logging

company_router = APIRouter(tags=["Компанії"], prefix="/companies")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def require_permissions(*required_permissions: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(
                *args,
                current_user: dict = Depends(get_current_user),
                role_manager: RoleManager = Depends(get_role_manager),
                **kwargs
        ):
            company_id = kwargs.get('company_id')
            logger.debug(f"Checking permissions for user {current_user['uid']}")
            logger.debug(f"Required permissions: {required_permissions}")
            logger.debug(f"Company ID: {company_id}")

            user_permissions = role_manager.get_user_permissions(current_user['uid'], company_id)
            logger.debug(f"User permissions: {user_permissions}")

            has_permission = role_manager.check_permissions(current_user['uid'], list(required_permissions), company_id)
            logger.debug(f"Permission check result: {has_permission}")

            if not has_permission:
                logger.warning(f"Permission denied for user {current_user['uid']}")
                raise HTTPException(status_code=403, detail="Не вистачає прав для виконання цієї дії")

            logger.debug(f"Permissions granted for user {current_user['uid']}")
            return await func(*args, current_user=current_user, role_manager=role_manager, **kwargs)

        return wrapper

    return decorator


@company_router.post("", response_model=CompanyResponse, summary="Створення компанії")
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


@company_router.get("", response_model=List[CompanyResponse], summary="Отримання компаній користувача")
async def get_companies(
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        companies = company_service.get_user_companies(current_user['uid'])
        return [CompanyResponse.from_orm(company) for company in companies]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@company_router.get("/{company_id}", response_model=CompanyResponse, summary="Отримання компанії користувача")
@require_permissions("view_company")
async def get_company(
        company_id: int = Path(..., description="ID компанії"),
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        company = company_service.get_user_company(company_id, current_user['uid'])
        if company is None:
            raise HTTPException(status_code=404, detail="Компанія не знайдена або була видалена")

        return CompanyResponse.from_orm(company)
    except ValueError as e:
        if "не знайдено" in str(e).lower():
            raise HTTPException(status_code=404, detail="Компанія не знайдена або була видалена")
        raise HTTPException(status_code=400, detail=str(e))


@company_router.put("/{company_id}", response_model=CompanyResponse, summary="Оновлення компанії")
@require_permissions("edit_company")
async def update_company(
        company_data: CompanyUpdate,
        company_id: int = Path(..., description="ID компанії"),
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        updated_company = company_service.update_company(company_id, company_data, current_user['uid'])
        return CompanyResponse.from_orm(updated_company)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@company_router.delete("/{company_id}", summary="Видалення компанії")
@require_permissions("delete_company")
async def delete_company(
        company_id: int = Path(..., description="ID компанії"),
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        return company_service.delete_company(company_id, current_user['uid'])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@company_router.post("/{company_id}/users", summary="Додавання користувача до компанії")
@require_permissions("manage_users")
async def add_user_to_company(
        company_id: int = Path(..., description="ІD компанії"),
        email: str = Query(..., description="Email користувача для додавання"),
        role_id: int = Query(..., description="ID ролі для призначення"),
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        return company_service.add_user_to_company(company_id, email, role_id, current_user['uid'])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@company_router.delete("/{company_id}/users/{email}", summary="Видалення користувача з компанії")
@require_permissions("manage_users")
async def remove_user_from_company(
        company_id: int = Path(..., description="ID компанії"),
        email: str = Path(..., description="Email користувача для видалення"),
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        return company_service.remove_user_from_company(company_id, email, current_user['uid'])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@company_router.post("/{company_id}/aquariums", response_model=AquariumResponse, summary="Створення нового акваріума")
@require_permissions("create_aquarium")
async def create_aquarium(
        aquarium_data: AquariumCreate,
        company_id: int = Path(..., description="ID компанії"),
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        new_aquarium = company_service.create_aquarium(company_id, aquarium_data, current_user['uid'])
        return AquariumResponse.from_orm(new_aquarium)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@company_router.get("/{company_id}/aquariums", response_model=List[AquariumResponse],
                    summary="Отримання списку акваріумів компанії")
@require_permissions("view_company_aquariums")
async def get_company_aquariums(
        company_id: int = Path(..., description="ID компанії"),
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        aquariums = company_service.get_company_aquariums(company_id, current_user['uid'])
        return [AquariumResponse.from_orm(aquarium) for aquarium in aquariums]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
