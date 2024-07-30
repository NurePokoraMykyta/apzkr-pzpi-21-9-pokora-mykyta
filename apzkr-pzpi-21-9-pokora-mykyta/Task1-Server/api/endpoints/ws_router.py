from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from services.connection_singleton import get_connection_manager
from services.device_feeding_service import DeviceFeedingService, get_device_feeding_service
from services.connection_manager import ConnectionManager
from data.session import db_session
import logging
import asyncio

logger = logging.getLogger(__name__)

ws_router = APIRouter()


@ws_router.websocket("/ws/{unique_address}")
async def websocket_endpoint(
        websocket: WebSocket,
        unique_address: str,
        db: Session = Depends(db_session),
        device_service: DeviceFeedingService = Depends(get_device_feeding_service),
        connection_manager: ConnectionManager = Depends(get_connection_manager)
):
    logger.info(f"WebSocket підключення від пристрою {unique_address}")
    await connection_manager.connect(websocket, unique_address)
    try:
        await device_service.sync_device_status(unique_address)

        while True:
            data = await websocket.receive_json()

            if data["action"] == "identify":
                await device_service.handle_device_identification(unique_address)
            elif data["action"] == "feed_result":
                try:
                    await device_service.handle_feed_result(unique_address, data["success"])
                except Exception as e:
                    logger.exception(
                        f"Помилка при обробці результату годування для пристрою {unique_address}: {str(e)}")
            elif data["action"] == "water_parameters":
                try:
                    device = device_service.get_device_by_address(unique_address)
                    await device_service.save_water_parameters(device.aquarium_id, data["parameters"])
                except Exception as e:
                    logger.exception(f"Помилка при збереженні параметрів води для пристрою {unique_address}: {str(e)}")
            else:
                logger.warning(f"Невідома дія від пристрою {unique_address}: {data['action']}")
    except WebSocketDisconnect:
        pass
        await handle_disconnect(unique_address, connection_manager)
    except Exception as e:
        logger.exception(f"Помилка при обробці WebSocket для пристрою {unique_address}: {str(e)}")
        await handle_disconnect(unique_address, connection_manager)


async def handle_disconnect(unique_address: str, connection_manager: ConnectionManager):
    await connection_manager.disconnect(unique_address)
    logger.info(f"Пристрій {unique_address} відключено від WebSocket")