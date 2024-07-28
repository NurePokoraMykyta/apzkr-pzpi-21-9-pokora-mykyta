import os

import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from api.endpoints.aquarium_feeding import aquarium_feeding_router
from api.endpoints.auth import auth_router
from api.endpoints.company import company_router
from api.endpoints.device import device_router
from api.endpoints.feeding_schedule import feeding_schedule_router
from api.endpoints.fish import fish_router
from api.endpoints.role import role_router
from api.endpoints.ws_router import ws_router
from core.config import settings
from data.session import setup_database, teardown_database
from services.connection_manager import ConnectionManager
from services.device_feeding_service import DeviceFeedingService
from data.session import db_session
from sqlalchemy.orm import Session

app = FastAPI(
    title="FinFare",
    version="1.0.0",
    description="Програмна система для догляду за рибками",
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection_manager = ConnectionManager()
scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup():
    setup_database()
    scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    await teardown_database()
    scheduler.shutdown()


api_router = APIRouter()
app.include_router(auth_router, prefix=settings.API_STR, tags=["Авторизація"])
app.include_router(role_router, prefix=settings.API_STR, tags=["Ролі"])
app.include_router(company_router, prefix=settings.API_STR, tags=["Компанії"])

app.include_router(fish_router, prefix=settings.API_STR, tags=["Риби"])
app.include_router(device_router, prefix=settings.API_STR, tags=["Пристрої"])
app.include_router(feeding_schedule_router, prefix=settings.API_STR, tags=["Розклади годування"])
app.include_router(aquarium_feeding_router, prefix=settings.API_STR, tags=["Годування акваріумів"])
app.include_router(ws_router, tags=["WebSocket"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


def get_device_feeding_service(db: Session = Depends(db_session)) -> DeviceFeedingService:
    return DeviceFeedingService(db, connection_manager)


async def scheduled_auto_feed():
    db = next(db_session())
    try:
        feeding_service = DeviceFeedingService(db, connection_manager)
        await feeding_service.auto_feed()
    finally:
        db.close()


scheduler.add_job(
    scheduled_auto_feed,
    trigger=IntervalTrigger(minutes=1),
    id='auto_feed_job',
    replace_existing=True
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)