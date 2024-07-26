from functools import wraps

from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List
from schemas.feeding_schemas import FeedingScheduleCreate, FeedingScheduleResponse
from services.device_feeding_service import DeviceFeedingService, get_device_feeding_service
from services.role_manager import RoleManager, get_role_manager
from api.user import get_current_user

aquarium_feeding_router = APIRouter(tags=["Годування акваріумів"], prefix="/aquariums/{aquarium_id}")


def require_permissions(*required_permissions: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(
                *args,
                current_user: dict = Depends(get_current_user),
                role_manager: RoleManager = Depends(get_role_manager),
                device_service: DeviceFeedingService = Depends(get_device_feeding_service),
                **kwargs
        ):
            company_id = 0
            aquarium_id = kwargs.get('aquarium_id')

            try:
                device = device_service.get_aquarium_device(aquarium_id)
                company_id = device.aquarium.company_id
            except ValueError:
                raise HTTPException(status_code=404, detail=company_id)

            user_permissions = role_manager.get_user_permissions(current_user['uid'], company_id)

            has_permission = role_manager.check_permissions(current_user['uid'], list(required_permissions), company_id)

            if not has_permission:
                raise HTTPException(status_code=403, detail="Недостатньо прав для виконання цієї дії")

            return await func(*args, current_user=current_user, role_manager=role_manager,
                              device_service=device_service, **kwargs)

        return wrapper

    return decorator


@aquarium_feeding_router.post("/feeding-schedules", response_model=FeedingScheduleResponse,
                              summary="Створення розкладу годування")
@require_permissions("manage_feeding_schedules")
async def create_feeding_schedule(
        aquarium_id: int = Path(..., description="ID акваріума"),
        schedule_data: FeedingScheduleCreate = ...,
        current_user: dict = Depends(get_current_user),
        device_service: DeviceFeedingService = Depends(get_device_feeding_service),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        new_schedule = device_service.add_feeding_schedule(aquarium_id, schedule_data)
        return FeedingScheduleResponse.from_orm(new_schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@aquarium_feeding_router.get("/feeding-schedules", response_model=List[FeedingScheduleResponse],
                             summary="Отримання розкладів годування акваріума")
@require_permissions("view_feeding_schedules")
async def get_feeding_schedules(
        aquarium_id: int = Path(..., description="ID акваріума"),
        current_user: dict = Depends(get_current_user),
        device_service: DeviceFeedingService = Depends(get_device_feeding_service),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        schedules = device_service.get_aquarium_feeding_schedules(aquarium_id)
        return [FeedingScheduleResponse.from_orm(schedule) for schedule in schedules]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@aquarium_feeding_router.post("/feed-now", summary="Негайне годування")
@require_permissions("manage_feeding")
async def feed_now(
        aquarium_id: int = Path(..., description="ID акваріума"),
        current_user: dict = Depends(get_current_user),
        device_service: DeviceFeedingService = Depends(get_device_feeding_service),
        role_manager: RoleManager = Depends(get_role_manager)
):
    try:
        result = await device_service.feed_now(aquarium_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))