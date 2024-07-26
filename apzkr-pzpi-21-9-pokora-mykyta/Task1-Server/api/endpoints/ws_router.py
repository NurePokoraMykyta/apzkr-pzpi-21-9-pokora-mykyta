from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from services.device_feeding_service import DeviceFeedingService, get_device_feeding_service
from services.connection_manager import ConnectionManager
from data.session import db_session
import logging

logger = logging.getLogger(__name__)

ws_router = APIRouter()

@ws_router.websocket("/ws/{unique_address}")
async def websocket_endpoint(
    websocket: WebSocket,
    unique_address: str,
    db: Session = Depends(db_session),
    device_service: DeviceFeedingService = Depends(get_device_feeding_service),
    connection_manager: ConnectionManager = Depends(lambda: ConnectionManager())
):
    await connection_manager.connect(websocket, unique_address)
    try:
        while True:
            data = await websocket.receive_json()
            if data["action"] == "feed_result":
                await device_service.handle_feed_result(unique_address, data["success"])
            elif data["action"] == "water_parameters":
                device = device_service.get_device_by_address(unique_address)
                if device:
                    await device_service.save_water_parameters(device.aquarium_id, data["parameters"])
                else:
                    logger.error(f"Пристрій не знайдено для адреси {unique_address}")
            elif data["action"] == "status_update":
                logger.info(f"Отримано оновлення статусу від пристрою {unique_address}: {data}")
            else:
                logger.warning(f"Невідома дія від пристрою {unique_address}: {data['action']}")
    except WebSocketDisconnect:
        connection_manager.disconnect(unique_address)
        logger.info(f"Пристрій {unique_address} відключився")
    except Exception as e:
        logger.error(f"Помилка при обробці WebSocket для пристрою {unique_address}: {str(e)}")
        connection_manager.disconnect(unique_address)