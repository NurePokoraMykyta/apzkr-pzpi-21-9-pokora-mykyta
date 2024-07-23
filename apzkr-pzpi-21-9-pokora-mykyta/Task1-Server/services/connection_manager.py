from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from typing import Dict


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, device_id: str):
        await websocket.accept()
        self.active_connections[device_id] = websocket

    def disconnect(self, device_id: str):
        self.active_connections.pop(device_id, None)

    async def send_command(self, device_id: str, message: dict):
        if device_id in self.active_connections:
            await self.active_connections[device_id].send_json(message)
        else:
            raise ValueError(f"Пристрій {device_id} не підключений")

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)
