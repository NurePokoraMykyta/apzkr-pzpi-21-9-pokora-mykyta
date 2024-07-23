from functools import wraps
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import List
from schemas.fish_schemas import FishCreate, FishUpdate, FishResponse
from services.company_service import CompanyService, get_company_manager
from services.role_manager import RoleManager, get_role_manager
from api.user import get_current_user
import logging

fish_router = APIRouter(tags=["Риби"], prefix="/aquariums/{aquarium_id}/fish")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def require_permissions(*required_permissions: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(
                *args,
                current_user: dict = Depends(get_current_user),
                role_manager: RoleManager = Depends(get_role_manager),
                company_service: CompanyService = Depends(get_company_manager),
                **kwargs
        ):
            company_id = kwargs.get('company_id')
            aquarium_id = kwargs.get('aquarium_id')

            try:
                company_service.get_company_aquarium(company_id, aquarium_id, current_user['uid'])
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))

            user_permissions = role_manager.get_user_permissions(current_user['uid'], company_id)
            logger.debug(f"User permissions: {user_permissions}")

            has_permission = role_manager.check_permissions(current_user['uid'], list(required_permissions), company_id)
            logger.debug(f"Permission check result: {has_permission}")

            if not has_permission:
                logger.warning(f"Permission denied for user {current_user['uid']}")
                raise HTTPException(status_code=403, detail="Не вистачає прав для виконання цієї дії")

            logger.debug(f"Permissions granted for user {current_user['uid']}")
            return await func(*args, current_user=current_user, role_manager=role_manager, company_service=company_service, **kwargs)

        return wrapper

    return decorator


@fish_router.post("", response_model=FishResponse, summary="Додавання нових риб в акваріум")
@require_permissions("manage_fish")
async def add_fish(
        fish_data: FishCreate,
        aquarium_id: int = Path(..., description="ID акваріума"),
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)

):
    try:
        new_fish = company_service.add_fish_to_aquarium(aquarium_id, fish_data, current_user['uid'])
        return FishResponse.from_orm(new_fish)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@fish_router.get("", response_model=List[FishResponse], summary="Отримання списку риб в акваріумі")
@require_permissions("view_fish")
async def get_aquarium_fish(
        aquarium_id: int = Path(..., description="ID акваріума"),
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)

):
    try:
        fish = company_service.get_aquarium_fish(aquarium_id, current_user['uid'])
        return [FishResponse.from_orm(f) for f in fish]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@fish_router.get("/{fish_id}", response_model=FishResponse, summary="Отримання інформації про конкретну рибу")
@require_permissions("view_fish")
async def get_fish(
        aquarium_id: int = Path(..., description="ID акваріума"),
        fish_id: int = Path(..., description="ID риби"),
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        fish = company_service.get_fish(aquarium_id, fish_id, current_user['uid'])
        return FishResponse.from_orm(fish)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@fish_router.put("/{fish_id}", response_model=FishResponse, summary="Оновлення інформації про рибу")
@require_permissions("manage_fish")
async def update_fish(
        fish_data: FishUpdate,
        aquarium_id: int = Path(..., description="ID акваріума"),
        fish_id: int = Path(..., description="ID риби"),
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)

):
    try:
        updated_fish = company_service.update_fish(aquarium_id, fish_id, fish_data, current_user['uid'])
        if updated_fish is None:
            return {"message": "Рибу видалено з акваріума"}
        return FishResponse.from_orm(updated_fish)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@fish_router.delete("/{fish_id}", summary="Видалення риби з акваріума")
@require_permissions("manage_fish")
async def remove_fish(
        aquarium_id: int = Path(..., description="ID акваріума"),
        fish_id: int = Path(..., description="ID риби"),
        quantity: int = Query(..., description="Кількість риб для видалення"),
        current_user: dict = Depends(get_current_user),
        company_service: CompanyService = Depends(get_company_manager),
        role_manager: RoleManager = Depends(get_role_manager)

):
    try:
        return company_service.remove_fish(aquarium_id, fish_id, quantity, current_user['uid'])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
