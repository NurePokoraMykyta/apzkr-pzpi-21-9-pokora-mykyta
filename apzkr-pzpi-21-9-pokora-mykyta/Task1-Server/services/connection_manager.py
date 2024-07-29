from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from typing import Dict
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.device_statuses: Dict[str, bool] = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, unique_address: str):
        await websocket.accept()
        async with self.lock:
            self.active_connections[unique_address] = websocket
        print(f"Пристрій {unique_address} підключився")

    async def disconnect(self, unique_address: str):
        async with self.lock:
            self.active_connections.pop(unique_address, None)
        print(f"Пристрій {unique_address} відключився")

    async def send_command(self, unique_address: str, message: dict):
        if unique_address in self.active_connections:
            await self.active_connections[unique_address].send_json(message)
        else:
            raise ValueError(f"Пристрій {unique_address} не підключений")

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)
