from fastapi import APIRouter, Depends, HTTPException

from schemas.user_schemas import BaseUserRequest, UserRegisterRequest, UserUpdateRequest
from services.auth_service import auth_service
from services.user_service import user_service
from api.user import get_current_user
from data.session import db_session
from sqlalchemy.orm import Session

auth_router = APIRouter(tags=["Авторизація"], prefix="/auth")


@auth_router.post("/register")
def register(user: UserRegisterRequest, db: Session = Depends(db_session)):
    try:
        user = auth_service.create_user(db, user.email, user.password, user.display_name)
        return {"message": "Користувача успішно створено", "uid": user.firebase_uid}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post("/login")
def login(user: BaseUserRequest):
    try:
        return auth_service.login_user(user.email, user.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@auth_router.post("/logout")
def logout(current_user: dict = Depends(get_current_user)):
    try:
        return auth_service.logout_user(current_user['uid'])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.get("/me")
def get_user(current_user: dict = Depends(get_current_user)):
    try:
        return user_service.get_user_by_uid(current_user['uid'])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@auth_router.put("/me")
def update_user(
        user: UserUpdateRequest,
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(db_session)
):
    try:
        updated_user = user_service.update_user(
            db,
            current_user['uid'],
            user
        )
        return {"message": "Користувача успішно оновлено", "user": updated_user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.delete("/me")
def delete_user(current_user: dict = Depends(get_current_user), db: Session = Depends(db_session)):
    try:
        return user_service.delete_user(db, current_user['uid'])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
