from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta

from data import db_session, WaterParameter
from data.models import IoTDevice, FoodPatch, FeedingSchedule, Aquarium
from typing import List

from schemas.Iot_device_schemas import IoTDeviceCreate, IoTDeviceUpdate
from schemas.feeding_schemas import FeedingScheduleCreate, FeedingScheduleUpdate

import logging

from schemas.water_parameter_schemas import WaterParameterCreate
from services.connection_manager import ConnectionManager
from fastapi import Depends

from services.connection_singleton import get_connection_manager

logger = logging.getLogger(__name__)


class DeviceFeedingService:
    def __init__(self, db: Session, connection_manager: ConnectionManager):
        self.db = db
        self.connection_manager = connection_manager

    def setup_device(self, aquarium_id: int, device_data: IoTDeviceCreate) -> IoTDevice:
        aquarium = self.db.query(Aquarium).filter(Aquarium.id == aquarium_id).first()
        if not aquarium:
            raise ValueError(f"Акваріум з id {aquarium_id} не знайдено")

        existing_device = self.db.query(IoTDevice).filter(
            IoTDevice.unique_address == device_data.unique_address).first()
        if existing_device:
            raise ValueError(f"Пристрій з адресою {device_data.unique_address} вже існує")

        existing_aquarium_device = self.db.query(IoTDevice).filter(
            IoTDevice.aquarium_id == aquarium_id).first()
        if existing_aquarium_device:
            raise ValueError(f"Акваріум з id {aquarium_id} вже має пристрій")

        new_device = IoTDevice(
            unique_address=device_data.unique_address,
            aquarium_id=aquarium_id,
            is_active=True
        )
        self.db.add(new_device)
        self.db.commit()
        self.db.refresh(new_device)

        logger.info(f"Новий пристрій успішно встановлено для акваріума {aquarium_id}")
        return new_device

    def get_aquarium(self, aquarium_id: int) -> Aquarium:
        aquarium = self.db.query(Aquarium).filter(Aquarium.id == aquarium_id).first()
        if not aquarium:
            raise ValueError(f"Акваріум з id {aquarium_id} не знайдено")
        return aquarium

    def get_aquarium_device(self, aquarium_id: int) -> IoTDevice:
        device = self.db.query(IoTDevice).filter(IoTDevice.aquarium_id == aquarium_id).first()
        if not device:
            raise ValueError(f"IoT пристрій не знайдено для акваріума {aquarium_id}")
        return device

    def update_device(self, aquarium_id: int, device_data: IoTDeviceUpdate) -> IoTDevice:
        device = self.get_aquarium_device(aquarium_id)
        if not device:
            raise ValueError(f"IoT пристрій не знайдено для акваріума {aquarium_id}")

        for key, value in device_data.dict(exclude_unset=True).items():
            setattr(device, key, value)

        try:
            self.db.commit()
            self.db.refresh(device)
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Помилка при оновленні пристрою: {str(e)}")

        return device

    async def activate_device(self, device_id: int) -> IoTDevice:
        device = self.db.query(IoTDevice).filter(IoTDevice.id == device_id).first()
        if not device:
            raise ValueError(f"IoT пристрій з id {device_id} не знайдено")

        logger.info(f"Спроба активувати пристрій {device.unique_address}")

        try:
            device.is_active = True
            self.db.commit()

            if device.unique_address in self.connection_manager.active_connections:
                await self.connection_manager.send_command(device.unique_address, {"action": "activate"})
            else:
                logger.warning(f"Пристрій {device.unique_address} не підключений по WebSocket")
        except Exception as e:
            logger.exception(f"Помилка при активації пристрою {device_id}: {str(e)}")
            self.db.rollback()
            raise

        return device

    async def deactivate_device(self, device_id: int) -> IoTDevice:
        device = self.db.query(IoTDevice).filter(IoTDevice.id == device_id).first()
        if not device:
            raise ValueError(f"IoT пристрій з id {device_id} не знайдено")

        try:
            device.is_active = False
            self.db.commit()

            if device.unique_address in self.connection_manager.active_connections:
                await self.connection_manager.send_command(device.unique_address, {"action": "deactivate"})
            else:
                logger.warning(f"Пристрій {device.unique_address} не підключений по WebSocket")
        except Exception as e:
            logger.exception(f"Помилка при деактивації пристрою {device_id}: {str(e)}")
            self.db.rollback()
            raise

        return device

    async def sync_device_status(self, unique_address: str):
        device = self.get_device_by_address(unique_address)
        if device:
            action = "activate" if device.is_active else "deactivate"
            await self.connection_manager.send_command(unique_address, {"action": action})
        else:
            logger.warning(f"Пристрій {unique_address} не знайдено при спробі синхронізації статусу")

    async def handle_device_identification(self, unique_address: str):
        device = self.get_device_by_address(unique_address)
        if device:
            await self.connection_manager.send_command(unique_address, {
                "action": "status_update",
                "is_active": device.is_active
            })
        else:
            logger.warning(f"Пристрій {unique_address} не знайдено в базі даних")

    def add_feeding_schedule(self, aquarium_id, schedule_data: FeedingScheduleCreate) -> FeedingSchedule:
        self.get_aquarium_device(aquarium_id)

        new_schedule = FeedingSchedule(
            food_type=schedule_data.food_type,
            scheduled_time=schedule_data.scheduled_time,
            aquarium_id=aquarium_id
        )
        self.db.add(new_schedule)
        self.db.commit()
        self.db.refresh(new_schedule)
        return new_schedule

    def get_aquarium_feeding_schedules(self, aquarium_id: int) -> List[FeedingSchedule]:
        schedules = self.db.query(FeedingSchedule).filter(FeedingSchedule.aquarium_id == aquarium_id).all()
        return schedules

    def get_feeding_schedule(self, schedule_id: int) -> FeedingSchedule:
        schedule = self.db.query(FeedingSchedule).filter(FeedingSchedule.id == schedule_id).first()
        if not schedule:
            raise ValueError("Розклад годування не знайдено")
        return schedule

    def update_feeding_schedule(self, schedule_id: int, schedule_data: FeedingScheduleUpdate) -> FeedingSchedule:
        schedule = self.get_feeding_schedule(schedule_id)
        for key, value in schedule_data.dict(exclude_unset=True).items():
            setattr(schedule, key, value)
        self.db.commit()
        self.db.refresh(schedule)
        return schedule

    def delete_feeding_schedule(self, schedule_id: int):
        schedule = self.get_feeding_schedule(schedule_id)
        self.db.delete(schedule)
        self.db.commit()

    async def send_feed_command(self, device_address: str, food_type: str, quantity: int):
        try:
            await self.connection_manager.send_command(device_address, {
                "action": "feed",
                "food_type": food_type,
                "quantity": quantity,
                "duration": 1.0  # Тривалість годування в секундах сервоприводу
            })
        except Exception as e:
            logger.error(f"Помилка при відправці команди на годування: {str(e)}")
            raise

    async def feed_now(self, aquarium_id: int) -> dict:
        device = self.get_aquarium_device(aquarium_id)
        if not device.is_active:
            return {"status": "error", "message": "Пристрій деактивовано"}

        food_patch = self.db.query(FoodPatch).filter(FoodPatch.iot_device_id == device.id).first()
        if not food_patch:
            return {"status": "error", "message": "Порцію корму не знайдено"}

        if food_patch.quantity <= 0:
            return {"status": "error", "message": "Корм закінчився"}

        try:
            await self.send_feed_command(device.unique_address, food_patch.food_type, 1)

            # Зменшуємо кількість корму в патчі тільки якщо команда відправлена успішно
            food_patch.quantity -= 1
            self.db.commit()

            return {"status": "success", "message": "Команда на годування відправлена"}
        except Exception as e:
            return {"status": "error", "message": f"Помилка при відправці команди на годування: {str(e)}"}

    async def auto_feed(self):
        current_time = datetime.now()
        one_minute_ago = current_time - timedelta(minutes=1)
        schedules = self.db.query(FeedingSchedule).filter(
            and_(
                FeedingSchedule.scheduled_time >= one_minute_ago,
                FeedingSchedule.scheduled_time <= current_time
            )
        ).all()

        for schedule in schedules:
            result = await self.feed_now(schedule.aquarium_id)
            if result["status"] == "error":
                logger.warning(
                    f"Помилка при автоматичному годуванні для акваріума {schedule.aquarium_id}: {result['message']}")
            else:
                logger.info(f"Команда на автоматичне годування відправлена для акваріума {schedule.aquarium_id}")

            # Обновляем время последнего кормления независимо от результата
            schedule.last_feed_time = current_time
            self.db.commit()

    async def handle_feed_result(self, device_id: str, success: bool):
        device = self.db.query(IoTDevice).filter(IoTDevice.unique_address == device_id).first()
        if not device:
            logger.error(f"Пристрій {device_id} не знайдено")
            return

        if success:
            logger.info(f"Годування успішно виконано пристроєм {device_id}")
            # На майбутнє можливо додам логіку для оновлення стану прострою або запису результату годування
        else:
            logger.error(f"Помилка при годуванні пристроєм {device_id}")
            # На майбутнє можливу додам логіку для обрабки помилок, наприклад, повернення корму в патч
            food_patch = self.db.query(FoodPatch).filter(FoodPatch.iot_device_id == device.id).first()
            if food_patch:
                food_patch.quantity += 1
                self.db.commit()
                logger.info(f"Кількість корму повернуто для пристрою {device_id}")

    def get_device_by_address(self, unique_address: str) -> IoTDevice:
        device = self.db.query(IoTDevice).filter(IoTDevice.unique_address == unique_address).first()
        if not device:
            raise ValueError(f"Пристрій з адресою {unique_address} не знайдено")
        return device

    async def save_water_parameters(self, aquarium_id: int, params: dict):
        try:
            water_params = WaterParameterCreate(
                ph=params['ph'],
                temperature=params['temperature'],
                salinity=params['salinity'],
                oxygen_level=params['oxygen_level'],
                aquarium_id=aquarium_id
            )
            water_param = WaterParameter(**water_params.dict())
            self.db.add(water_param)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Помилка при збереженні параметрів води для акваріума {aquarium_id}: {str(e)}")
            raise


def get_device_feeding_service(
        db: Session = Depends(db_session),
        connection_manager: ConnectionManager = Depends(get_connection_manager)
) -> DeviceFeedingService:
    return DeviceFeedingService(db, connection_manager)
