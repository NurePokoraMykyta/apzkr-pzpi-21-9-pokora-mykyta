from functools import wraps

from fastapi import APIRouter, Depends, HTTPException, Path
from schemas.feeding_schemas import FeedingScheduleResponse, FeedingScheduleUpdate
from services.device_feeding_service import DeviceFeedingService, get_device_feeding_service
from services.role_manager import RoleManager, get_role_manager
from api.user import get_current_user

feeding_schedule_router = APIRouter(tags=["Розклади годування"], prefix="/feeding-schedules")


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
            schedule_id = kwargs.get('schedule_id')
            try:
                schedule = device_service.get_feeding_schedule(schedule_id)
                company_id = schedule.aquarium.company_id
            except ValueError:
                raise HTTPException(status_code=404, detail="Розклад годування не знайдено")

            user_permissions = role_manager.get_user_permissions(current_user['uid'], company_id)

            has_permission = role_manager.check_permissions(current_user['uid'], list(required_permissions), company_id)

            if not has_permission:
                raise HTTPException(status_code=403, detail="Недостатньо прав для виконання цієї дії")

            return await func(*args, current_user=current_user, role_manager=role_manager,
                              device_service=device_service, **kwargs)

        return wrapper

    return decorator


@feeding_schedule_router.get("/{schedule_id}", response_model=FeedingScheduleResponse,
                             summary="Отримання інформації про розклад годування")
@require_permissions("view_feeding_schedules")
async def get_feeding_schedule(
        schedule_id: int = Path(..., description="ID розкладу годування"),
        current_user: dict = Depends(get_current_user),
        device_service: DeviceFeedingService = Depends(get_device_feeding_service),
        role_manager: RoleManager = Depends(get_role_manager)

):
    try:
        schedule = device_service.get_feeding_schedule(schedule_id)
        return FeedingScheduleResponse.from_orm(schedule)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@feeding_schedule_router.put("/{schedule_id}", response_model=FeedingScheduleResponse,
                             summary="Оновлення розкладу годування")
@require_permissions("manage_feeding_schedules")
async def update_feeding_schedule(
        schedule_id: int = Path(..., description="ID розкладу годування"),
        schedule_data: FeedingScheduleUpdate = ...,
        current_user: dict = Depends(get_current_user),
        device_service: DeviceFeedingService = Depends(get_device_feeding_service),
        role_manager: RoleManager = Depends(get_role_manager)

):
    try:
        updated_schedule = device_service.update_feeding_schedule(schedule_id, schedule_data)
        return FeedingScheduleResponse.from_orm(updated_schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@feeding_schedule_router.delete("/{schedule_id}", summary="Видалення розкладу годування")
@require_permissions("manage_feeding_schedules")
async def delete_feeding_schedule(
        schedule_id: int = Path(..., description="ID розкладу годування"),
        current_user: dict = Depends(get_current_user),
        device_service: DeviceFeedingService = Depends(get_device_feeding_service),
        role_manager: RoleManager = Depends(get_role_manager)

):
    try:
        device_service.delete_feeding_schedule(schedule_id)
        return {"message": "Розклад годування успішно видалено"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))