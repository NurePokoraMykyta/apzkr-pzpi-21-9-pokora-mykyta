from fastapi import APIRouter, Depends, HTTPException

from schemas.user_schemas import BaseUserRequest, UserRegisterRequest, UserUpdateRequest
from services.auth_service import auth_service
from services.user_service import user_service
from api.user import get_current_user
from data.session import db_session
from sqlalchemy.orm import Session

auth_router = APIRouter(tags=["Авторизація"], prefix="/auth")


@auth_router.post("/register", summary="Реєстрація користувача")
def register(user: UserRegisterRequest, db: Session = Depends(db_session)):
    try:
        user = auth_service.create_user(db, user.email, user.password, user.display_name)
        return {"message": "Користувача успішно створено", "uid": user.firebase_uid}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post("/login", summary="Авторизація користувача")
def login(user: BaseUserRequest):
    try:
        return auth_service.login_user(user.email, user.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@auth_router.post("/logout", summary="Вихід користувача")
def logout(current_user: dict = Depends(get_current_user)):
    try:
        return auth_service.logout_user(current_user['uid'])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.get("/me", summary="Отримання даних користувача")
def get_user(user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.get_user_by_uid(user_service.current_user['uid'])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@auth_router.put("/me", summary="Оновлення даних користувача")
def update_user(
    user: UserUpdateRequest,
    user_service: UserService = Depends(get_user_service)
):
    try:
        updated_user = user_service.update_user(user)
        return {"message": "Користувача успішно оновлено", "user": updated_user}
    except HTTPException as he:
        logger.error(f"HTTP ошибка при обновлении пользователя: {he.detail}")
        raise he
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при обновлении пользователя: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@auth_router.delete("/me", summary="Видалення користувача")
def delete_user(user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.delete_user()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
