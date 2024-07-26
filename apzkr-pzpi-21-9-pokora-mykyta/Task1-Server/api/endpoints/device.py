from functools import wraps

from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List

from schemas.Iot_device_schemas import IoTDeviceResponse, IoTDeviceUpdate, IoTDeviceCreate
from services import get_role_manager, RoleManager
from services.device_feeding_service import DeviceFeedingService, get_device_feeding_service
from api.user import get_current_user

device_router = APIRouter(tags=["Пристрої"], prefix="/devices")


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
            aquarium_id = kwargs.get('aquarium_id')
            if aquarium_id is None:
                raise HTTPException(status_code=400, detail="Не вказано ID акваріума")

            try:
                aquarium = device_service.get_aquarium(aquarium_id)
                company_id = aquarium.company_id
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))

            #user_permissions = role_manager.get_user_permissions(current_user['uid'], company_id)

            has_permission = role_manager.check_permissions(current_user['uid'], list(required_permissions), company_id)

            if not has_permission:
                raise HTTPException(status_code=403, detail="Недостатньо прав для виконання цієї дії")

            return await func(*args, current_user=current_user, role_manager=role_manager,
                              device_service=device_service, **kwargs)

        return wrapper

    return decorator


@device_router.post("/{aquarium_id}", response_model=IoTDeviceResponse, summary="Встановлення нового пристрою")
@require_permissions("manage_devices")
async def setup_device(
        aquarium_id: int = Path(..., description="ID акваріума"),
        device_data: IoTDeviceCreate = ...,
        current_user: dict = Depends(get_current_user),
        device_service: DeviceFeedingService = Depends(get_device_feeding_service),
        role_manager: RoleManager = Depends(get_role_manager)

):
    try:
        new_device = device_service.setup_device(aquarium_id, device_data)
        return IoTDeviceResponse.from_orm(new_device)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@device_router.get("/{aquarium_id}", response_model=IoTDeviceResponse, summary="Отримання інформації про пристрій")
@require_permissions("view_devices")
async def get_device(
        aquarium_id: int = Path(..., description="ID акваріума"),
        current_user: dict = Depends(get_current_user),
        device_service: DeviceFeedingService = Depends(get_device_feeding_service),
        role_manager: RoleManager = Depends(get_role_manager)

):
    try:
        device = device_service.get_aquarium_device(aquarium_id)
        return IoTDeviceResponse.from_orm(device)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@device_router.put("/{aquarium_id}", response_model=IoTDeviceResponse, summary="Оновлення інформації про пристрій")
@require_permissions("manage_devices")
async def update_device(
        aquarium_id: int = Path(..., description="ID акваріума"),
        device_data: IoTDeviceUpdate = ...,
        current_user: dict = Depends(get_current_user),
        device_service: DeviceFeedingService = Depends(get_device_feeding_service),
        role_manager: RoleManager = Depends(get_role_manager)

):
    try:
        updated_device = device_service.update_device(aquarium_id, device_data)
        return IoTDeviceResponse.from_orm(updated_device)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@device_router.post("/{aquarium_id}/activate", response_model=IoTDeviceResponse, summary="Активація пристрою")
@require_permissions("manage_devices")
async def activate_device(
        aquarium_id: int = Path(..., description="ID акваріума"),
        current_user: dict = Depends(get_current_user),
        device_service: DeviceFeedingService = Depends(get_device_feeding_service),
        role_manager: RoleManager = Depends(get_role_manager)

):
    try:
        device = device_service.get_aquarium_device(aquarium_id)
        if not device:
            raise HTTPException(status_code=404, detail="Пристрій не знайдено")
        if device.is_active:
            raise HTTPException(status_code=400, detail="Пристрій вже активовано")
        activated_device = await device_service.activate_device(device.id)
        return IoTDeviceResponse.from_orm(activated_device)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@device_router.post("/{aquarium_id}/deactivate", response_model=IoTDeviceResponse, summary="Деактивація пристрою")
@require_permissions("manage_devices")
async def deactivate_device(
        aquarium_id: int = Path(..., description="ID акваріума"),
        current_user: dict = Depends(get_current_user),
        device_service: DeviceFeedingService = Depends(get_device_feeding_service),
        role_manager: RoleManager = Depends(get_role_manager)

):
    try:
        device = device_service.get_aquarium_device(aquarium_id)
        if not device:
            raise HTTPException(status_code=404, detail="Пристрій не знайдено")
        if not device.is_active:
            raise HTTPException(status_code=400, detail="Пристрій вже деактивовано")
        deactivated_device = await device_service.deactivate_device(device.id)
        return IoTDeviceResponse.from_orm(deactivated_device)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))