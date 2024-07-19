from firebase_admin import auth as firebase_auth
from firebase_admin.auth import (
    UserNotFoundError,
    EmailAlreadyExistsError,
    PhoneNumberAlreadyExistsError,
    UidAlreadyExistsError
)
from sqlalchemy.orm import Session

from data.models.user import User
from schemas.user_schemas import UserUpdateRequest


class UserService:
    @staticmethod
    def get_user_by_email(email: str):
        try:
            return firebase_auth.get_user_by_email(email)
        except UserNotFoundError:
            raise ValueError("Користувача не знайдено")

    @staticmethod
    def get_user_by_uid(db: Session, uid: str):
        try:
            return db.query(User).filter(User.firebase_uid == uid).first()
        except UserNotFoundError:
            raise ValueError("Користувача не знайдено")

    @staticmethod
    def update_user(db: Session, uid: str, update_data: UserUpdateRequest):
        try:
            db_user = db.query(User).filter(User.firebase_uid == uid).first()
            if update_data.display_name:
                firebase_auth.update_user(uid, display_name=update_data.display_name)
                db_user.display_name = update_data.display_name
            if update_data.email:
                firebase_auth.update_user(uid, email=update_data.email)
                db_user.email = update_data.email
            if update_data.phone_number:
                firebase_auth.update_user(uid, phone_number=update_data.phone_number)
                db_user.phone_number = update_data.phone_number
            db.commit()
            db.refresh(db_user)
            return firebase_auth.update_user(uid, **update_data.dict())
        except UserNotFoundError:
            raise ValueError("Користувача не знайдено")
        except EmailAlreadyExistsError:
            raise ValueError("Електронна пошта вже існує")
        except PhoneNumberAlreadyExistsError:
            raise ValueError("Номер телефону вже існує")
        except UidAlreadyExistsError:
            raise ValueError("UID вже існує")
        except Exception as e:
            raise ValueError(f"Помилка під час оновлення користувача: {str(e)}")

    @staticmethod
    def delete_user(db: Session, uid: str):
        try:
            firebase_auth.delete_user(uid)
            db_user = db.query(User).filter(User.firebase_uid == uid).first()
            if db_user:
                db.delete(db_user)
                db.commit()
            return {"message": "Користувача успішно видалено"}
        except UserNotFoundError:
            raise ValueError("Користувача не знайдено")
        except Exception as e:
            raise ValueError(f"Помилка під час видалення користувача: {str(e)}")


user_service = UserService()