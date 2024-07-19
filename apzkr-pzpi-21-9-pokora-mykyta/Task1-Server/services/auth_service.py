from firebase_admin import auth as firebase_auth
from firebase_admin.auth import (
    EmailAlreadyExistsError,
    PhoneNumberAlreadyExistsError,
    UserNotFoundError,
    InvalidIdTokenError,
    CertificateFetchError
)
from core.firebase import pyrebase_auth
from data.models.user import User, UserStatus
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from data.session import db_session


class AuthService:
    @staticmethod
    def create_user(db: Session, email: str, password: str, display_name: str = None):
        try:
            firebase_user = pyrebase_auth.create_user_with_email_and_password(email, password)
            if display_name:
                firebase_auth.update_user(firebase_user['localId'], display_name=display_name)

            db_user = User(
                firebase_uid=firebase_user['localId'],
                email=email,
                status=UserStatus.ACTIVE
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            return db_user
        except firebase_auth.EmailAlreadyExistsError:
            raise ValueError("Електронна пошта вже існує")
        except firebase_auth.PhoneNumberAlreadyExistsError:
            raise ValueError("Номер телефону вже існує")
        except IntegrityError:
            db.rollback()
            raise ValueError("Помилка при збереженні користувача в базі даних")
        except Exception as e:
            db.rollback()
            raise ValueError(f"Помилка під час створення користувача: {str(e)}")

    @staticmethod
    def login_user(email: str, password: str):
        try:
            user = pyrebase_auth.sign_in_with_email_and_password(email, password)
            return {"access_token": user['idToken'], "token_type": "bearer"}
        except Exception as e:
            raise ValueError("Неправильні облікові дані")

    @staticmethod
    def logout_user(token: str):
        try:
            firebase_auth.revoke_refresh_tokens(token)
            return {"message": "Успішно вийшли з системи"}
        except UserNotFoundError:
            raise ValueError("Користувача не знайдено")
        except Exception as e:
            raise ValueError(f"Помилка під час виходу: {str(e)}")

    @staticmethod
    def verify_token(token: str):
        try:
            decoded = firebase_auth.verify_id_token(token)
            print(decoded)
            return decoded
        except InvalidIdTokenError:
            raise ValueError("Недійсний токен")
        except CertificateFetchError:
            raise ValueError("Не вдалося отримати сертифікати для перевірки токена")
        except Exception as e:
            raise ValueError(f"Помилка під час перевірки токена: {str(e)}")


auth_service = AuthService()