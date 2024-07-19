from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth_service import auth_service

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    token: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)],
) -> Optional[dict]:

    try:
        if not token:
            raise ValueError("Токен не надано")
        user = auth_service.verify_token(token.credentials)
        if user is None:
            raise ValueError("Не вдалося отримати дані користувача з токена")
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недійсний токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
