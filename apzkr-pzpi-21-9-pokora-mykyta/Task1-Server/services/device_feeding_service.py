from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta

from data import db_session
from data.models import IoTDevice, FoodPatch, FeedingSchedule, Aquarium
from typing import List

from schemas.Iot_device_schemas import IoTDeviceCreate, IoTDeviceUpdate
from schemas.feeding_schemas import FeedingScheduleCreate, FeedingScheduleUpdate

import logging

from schemas.water_parameter_schemas import WaterParameterCreate
from services.connection_manager import ConnectionManager
from fastapi import Depends

logger = logging.getLogger(__name__)


class DeviceFeedingService:
    def __init__(self, db: Session, connection_manager: ConnectionManager):
        self.db = db
        self.connection_manager = connection_manager

    def setup_device(self, aquarium_id: int, device_data: IoTDeviceCreate) -> IoTDevice:
        aquarium = self.db.query(Aquarium).filter(Aquarium.id == aquarium_id).first()
        if not aquarium:
            logger.error(f"Акваріум з id {aquarium_id} не знайдено")
            raise ValueError(f"Акваріум з id {aquarium_id} не знайдено")

        existing_device = self.db.query(IoTDevice).filter(
            IoTDevice.unique_address == device_data.unique_address).first()
        if existing_device:
            logger.error(f"Пристрій з адресою {device_data.unique_address} вже існує")
            raise ValueError(f"Пристрій з адресою {device_data.unique_address} вже існує")

        existing_aquarium_device = self.db.query(IoTDevice).filter(
            IoTDevice.aquarium_id == aquarium_id).first()
        if existing_aquarium_device:
            logger.error(f"Акваріум з id {aquarium_id} вже має пристрій")
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
            logger.error(f"Акваріум з id {aquarium_id} не знайдено")
            raise ValueError(f"Акваріум з id {aquarium_id} не знайдено")
        return aquarium

    def get_aquarium_device(self, aquarium_id: int) -> IoTDevice:
        device = self.db.query(IoTDevice).filter(IoTDevice.aquarium_id == aquarium_id).first()
        if not device:
            logger.error(f"IoT пристрій не знайдено для акваріума {aquarium_id}")
            raise ValueError(f"IoT пристрій не знайдено для акваріума {aquarium_id}")
        return device

    def update_device(self, aquarium_id: int, device_data: IoTDeviceUpdate) -> IoTDevice:
        device = self.get_aquarium_device(aquarium_id)
        if not device:
            logger.error(f"IoT пристрій не знайдено для акваріума {aquarium_id}")
            raise ValueError(f"IoT пристрій не знайдено для акваріума {aquarium_id}")

        for key, value in device_data.dict(exclude_unset=True).items():
            setattr(device, key, value)

        try:
            self.db.commit()
            self.db.refresh(device)
            logger.info(f"Оновлено пристрій для акваріума {aquarium_id}")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Помилка при оновленні пристрою для акваріума {aquarium_id}: {str(e)}")
            raise ValueError(f"Помилка при оновленні пристрою: {str(e)}")

        return device

    async def activate_device(self, device_id: int) -> IoTDevice:
        device = self.db.query(IoTDevice).filter(IoTDevice.id == device_id).first()
        if not device:
            logger.error(f"IoT пристрій з id {device_id} не знайдено")
            raise ValueError(f"IoT пристрій з id {device_id} не знайдено")

        try:
            await self.connection_manager.send_command(device.unique_address, {"action": "activate"})
            device.is_active = True
            self.db.commit()
            logger.info(f"Пристрій {device_id} успішно активовано")
        except Exception as e:
            logger.error(f"Помилка при активації пристрою {device_id}: {str(e)}")
            raise ValueError(f"Помилка при активації пристрою: {str(e)}")
        return device

    async def deactivate_device(self, device_id: int) -> IoTDevice:
        device = self.db.query(IoTDevice).filter(IoTDevice.id == device_id).first()
        if not device:
            logger.error(f"IoT пристрій з id {device_id} не знайдено")
            raise ValueError(f"IoT пристрій з id {device_id} не знайдено")

        try:
            await self.connection_manager.send_command(device.unique_address, {"action": "deactivate"})
            device.is_active = False
            self.db.commit()
            logger.info(f"Пристрій {device_id} успішно деактивовано")
        except Exception as e:
            logger.error(f"Помилка при деактивації пристрою {device_id}: {str(e)}")
            raise ValueError(f"Помилка при деактивації пристрою: {str(e)}")
        return device

    def add_feeding_schedule(self, aquarium_id, schedule_data: FeedingScheduleCreate) -> FeedingSchedule:
        self.get_aquarium_device(schedule_data.aquarium_id)

        new_schedule = FeedingSchedule(
            food_type=schedule_data.food_type,
            scheduled_time=schedule_data.scheduled_time,
        )
        self.db.add(new_schedule)
        self.db.commit()
        self.db.refresh(new_schedule)
        logger.info(f"Додано новий розклад годування для акваріума {schedule_data.aquarium_id}")
        return new_schedule

    def get_aquarium_feeding_schedules(self, aquarium_id: int) -> List[FeedingSchedule]:
        schedules = self.db.query(FeedingSchedule).filter(FeedingSchedule.aquarium_id == aquarium_id).all()
        logger.info(f"Отримано {len(schedules)} розкладів годування для акваріума {aquarium_id}")
        return schedules

    def get_feeding_schedule(self, schedule_id: int) -> FeedingSchedule:
        schedule = self.db.query(FeedingSchedule).filter(FeedingSchedule.id == schedule_id).first()
        if not schedule:
            logger.error(f"Розклад годування з id {schedule_id} не знайдено")
            raise ValueError("Розклад годування не знайдено")
        return schedule

    def update_feeding_schedule(self, schedule_id: int, schedule_data: FeedingScheduleUpdate) -> FeedingSchedule:
        schedule = self.get_feeding_schedule(schedule_id)
        for key, value in schedule_data.dict(exclude_unset=True).items():
            setattr(schedule, key, value)
        self.db.commit()
        self.db.refresh(schedule)
        logger.info(f"Оновлено розклад годування {schedule_id}")
        return schedule

    def delete_feeding_schedule(self, schedule_id: int):
        schedule = self.get_feeding_schedule(schedule_id)
        self.db.delete(schedule)
        self.db.commit()
        logger.info(f"Видалено розклад годування {schedule_id}")

    async def send_feed_command(self, device_address: str, food_type: str, quantity: int):
        try:
            await self.connection_manager.send_command(device_address, {
                "action": "feed",
                "food_type": food_type,
                "quantity": quantity,
                "duration": 1.0  # Тривалість годування в секундах сервоприводу
            })
            logger.info(f"Команда на годування відправлена пристрою {device_address}")
        except Exception as e:
            logger.error(f"Помилка при відправці команди на годування: {str(e)}")
            raise

    async def feed_now(self, aquarium_id: int) -> dict:
        device = self.get_aquarium_device(aquarium_id)
        if not device.is_active:
            logger.warning(f"Пристрій для акваріума {aquarium_id} деактивовано")
            return {"status": "error", "message": "Пристрій деактивовано"}

        food_patch = self.db.query(FoodPatch).filter(FoodPatch.iot_device_id == device.id).first()
        if not food_patch:
            logger.error(f"Порцію корму не знайдено для пристрою {device.id}")
            return {"status": "error", "message": "Порцію корму не знайдено"}

        if food_patch.quantity <= 0:
            logger.warning(f"Корм закінчився в пристрої {device.id}")
            return {"status": "error", "message": "Корм закінчився"}

        try:
            await self.send_feed_command(device.unique_address, food_patch.food_type, 1)

            # Зменшуємо кількість корму в патчі тільки якщо команда відправлена успішно
            food_patch.quantity -= 1
            self.db.commit()

            logger.info(f"Команда на годування відправлена для акваріума {aquarium_id}")
            return {"status": "success", "message": "Команда на годування відправлена"}
        except Exception as e:
            logger.error(f"Помилка при відправці команди на годування для акваріума {aquarium_id}: {str(e)}")
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
            logger.info(f"Виконання автоматичного годування для розкладу {schedule.id}")
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
            logger.error(f"Пристрій з адресою {unique_address} не знайдено")
            raise ValueError(f"Пристрій з адресою {unique_address} не знайдено")
        return device

    async def save_water_parameters(self, water_params: WaterParameterCreate):
        try:
            water_param = WaterParameterCreate(
                ph=water_params.ph,
                temperature=water_params.temperature,
                ammonia=water_params.ammonia,
                nitrite=water_params.nitrite,
                nitrate=water_params.nitrate,
                aquarium_id=water_params.aquarium_id
            )
            self.db.add(water_param)
            self.db.commit()
            logger.info(f"Параметри води збережено для акваріума {water_params.aquarium_id}")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Помилка при збереженні параметрів води для акваріума {water_params.aquarium_id}: {str(e)}")
            raise


def get_device_feeding_service(
        db: Session = Depends(db_session),
        connection_manager: ConnectionManager = Depends(lambda: ConnectionManager())
) -> DeviceFeedingService:
    return DeviceFeedingService(db, connection_manager)
