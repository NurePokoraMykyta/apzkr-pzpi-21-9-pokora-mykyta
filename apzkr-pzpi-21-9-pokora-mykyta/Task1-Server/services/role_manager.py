from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from functools import wraps
from typing import List, Callable, Optional

from api.user import get_current_user
from data.models.role import Role
from data.models.user import User, user_companies
from data.session import db_session

ADMIN_ROLE = "адмін"
OWNER_ROLE = "власник"

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from functools import wraps
from typing import List, Callable, Optional

from api.user import get_current_user
from data.models.role import Role
from data.models.user import User, user_companies
from data.session import db_session

ADMIN_ROLE = "адмін"
OWNER_ROLE = "власник"


class RoleManager:
    def __init__(self, db: Session):
        self.db = db
        self.create_defaults_roles()

    def create_defaults_roles(self):
        for role_name, permissions in [
            (ADMIN_ROLE, ["manage_company", "manage_users", "manage_roles"]),
            (OWNER_ROLE, ["*"])
        ]:
            role = self.db.query(Role).filter(Role.name == role_name).first()
            if not role:
                self.create_role(role_name, f"Default {role_name} role", permissions)

    def create_role(self, name: str, description: str = None, permissions: List[str] = None, company_id: int = None):
        new_role = Role(name=name, description=description, permissions=permissions or [])
        self.db.add(new_role)
        self.db.flush()

        if company_id:
            company_role = user_companies.insert().values(
                company_id=company_id,
                role_id=new_role.id
            )
            self.db.execute(company_role)

        self.db.commit()
        self.db.refresh(new_role)
        return new_role

    def assign_role(self, user_id: int, role_id: int, company_id: int):
        user_company = self.db.query(user_companies).filter(
            user_companies.c.user_id == user_id,
            user_companies.c.company_id == company_id
        ).first()

        if not user_company:
            self.db.execute(user_companies.insert().values(
                user_id=user_id,
                company_id=company_id,
                role_id=role_id
            ))
        else:
            self.db.execute(
                user_companies.update().where(
                    and_(user_companies.c.user_id == user_id,
                         user_companies.c.company_id == company_id)
                ).values(role_id=role_id)
            )
        self.db.commit()

    def get_user_permissions(self, firebase_uid: str, company_id: int):
        user = self.db.query(User).filter(User.firebase_uid == firebase_uid).first()
        if not user:
            return []

        user_role = self.db.query(Role).join(
            user_companies,
            and_(
                user_companies.c.role_id == Role.id,
                user_companies.c.user_id == user.id,
                user_companies.c.company_id == company_id
            )
        ).first()

        if not user_role:
            return []

        return user_role.permissions

    def check_permissions(self, firebase_uid: str, required_permissions: List[str], company_id: int = None) -> bool:
        user_permissions = self.get_user_permissions(firebase_uid, company_id)
        return '*' in user_permissions or all(perm in user_permissions for perm in required_permissions)

    def get_company_roles(self, company_id: int):
        return self.db.query(Role).filter(
            user_companies.c.company_id == company_id
        )

    def get_company_role(self, company_id: int, role_id: int):
        role = self.db.query(Role).join(user_companies, Role.id == user_companies.c.role_id).filter(
            and_(user_companies.c.company_id == company_id, Role.id == role_id)
        ).first()
        if not role:
            raise ValueError("Роль не знайдено для даної компанії")
        return role

    def assign_owner_role(self, firebase_uid: str, company_id: int):
        user = self.db.query(User).filter(User.firebase_uid == firebase_uid).first()
        if not user:
            raise ValueError("Користувача не знайдено")

        owner_role = self.db.query(Role).filter(Role.name == OWNER_ROLE).first()
        if not owner_role:
            raise ValueError("Роль власника не знайдено")

        user_company = user_companies.insert().values(
            user_id=user.id,
            company_id=company_id,
            role_id=owner_role.id
        )
        self.db.execute(user_company)
        self.db.commit()

    def has_company_access(self, firebase_uid: str, company_id: int) -> bool:
        user = self.db.query(User).filter(User.firebase_uid == firebase_uid).first()
        if not user:
            return False

        user_company = self.db.query(user_companies).filter(
            and_(user_companies.c.user_id == user.id,
                 user_companies.c.company_id == company_id)
        ).first()
        return user_company is not None


def get_role_manager(db: Session = Depends(db_session)):
    return RoleManager(db)


def require_permissions(*required_permissions: str):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(
                *args,
                current_user: dict = Depends(get_current_user),
                role_manager: RoleManager = Depends(get_role_manager),
                **kwargs
        ):
            company_id = kwargs.get('company_id')
            if company_id:
                if not role_manager.check_permissions(current_user['uid'], list(required_permissions), company_id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Не вистачає прав для виконання цієї дії"
                    )
            return await func(*args, **kwargs)

        return wrapper

    return decorator
