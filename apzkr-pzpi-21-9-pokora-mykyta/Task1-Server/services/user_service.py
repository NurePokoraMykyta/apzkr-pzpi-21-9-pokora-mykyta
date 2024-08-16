from firebase_admin import auth as firebase_auth
from firebase_admin.auth import (
    UserNotFoundError,
    EmailAlreadyExistsError,
    PhoneNumberAlreadyExistsError,
    UidAlreadyExistsError
)
from sqlalchemy.orm import Session

from api.user import get_current_user
from data import db_session
from data.models.user import User
from schemas.user_schemas import UserUpdateRequest
from fastapi import Depends


class UserService:
    def __init__(self, db: Session, current_user: dict):
        self.db = db
        self.current_user = current_user

    def get_user_by_email(self, email: str):
        try:
            return firebase_auth.get_user_by_email(email)
        except UserNotFoundError:
            raise ValueError("Користувача не знайдено")

    def get_user_by_uid(self, uid: str):
        try:
            return self.db.query(User).filter(User.firebase_uid == uid).first()
        except UserNotFoundError:
            raise ValueError("Користувача не знайдено")

    def update_user(self, update_data: UserUpdateRequest):
        try:
            db_user = self.db.query(User).filter(User.firebase_uid == self.current_user['uid']).first()
            if update_data.display_name:
                firebase_auth.update_user(self.current_user['uid'], display_name=update_data.display_name)
                db_user.display_name = update_data.display_name
            if update_data.email:
                firebase_auth.update_user(self.current_user['uid'], email=update_data.email)
                db_user.email = update_data.email
            if update_data.phone_number:
                firebase_auth.update_user(self.current_user['uid'], phone_number=update_data.phone_number)
                db_user.phone_number = update_data.phone_number
            self.db.commit()
            self.db.refresh(db_user)
            return firebase_auth.update_user(self.current_user['uid'], **update_data.dict())
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

    def delete_user(self):
        try:
            firebase_auth.delete_user(self.current_user['uid'])
            db_user = self.db.query(User).filter(User.firebase_uid == self.current_user['uid']).first()
            if db_user:
                self.db.delete(db_user)
                self.db.commit()
            return {"message": "Користувача успішно видалено"}
        except UserNotFoundError:
            raise ValueError("Користувача не знайдено")
        except Exception as e:
            raise ValueError(f"Помилка під час видалення користувача: {str(e)}")


def get_user_service(
        db: Session = Depends(db_session),
        current_user: dict = Depends(get_current_user)
) -> UserService:
    return UserService(db, current_user)
