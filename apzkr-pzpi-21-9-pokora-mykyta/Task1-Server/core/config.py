import os
import pathlib
from functools import lru_cache
from dotenv import load_dotenv

from pydantic_settings import BaseSettings
basedir = pathlib.Path(__file__).parents[1]
load_dotenv(basedir / ".env")


class Settings(BaseSettings):
    app_name: str = "FinFare"
    FRONTEND_URL: str = os.getenv("FRONTEND_URL")
    API_STR: str = "/api"

    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_SERVER: str = os.getenv("DB_SERVER")
    DB_NAME: str = os.getenv("DB_NAME")

    FIREBASE_CREDENTIALS: str = str(os.getenv("FIREBASE_CREDENTIALS", basedir / "finfare-credentials.json"))

    FIREBASE_CONFIG: dict = {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID"),
        "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    }

    class Config:
        env_file = "../.env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
