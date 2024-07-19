import os

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints.auth import auth_router
from core.config import settings
from data.session import setup_database, teardown_database

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


@app.on_event("startup")
async def startup():
    setup_database()


@app.on_event("shutdown")
async def shutdown():
    await teardown_database()


api_router = APIRouter()
app.include_router(auth_router, prefix=settings.API_STR, tags=["Авторизація"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
