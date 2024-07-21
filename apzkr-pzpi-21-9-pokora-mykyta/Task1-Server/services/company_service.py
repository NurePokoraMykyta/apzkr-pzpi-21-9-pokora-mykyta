from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from data.session import db_session
from data.models.company import Company
from data.models.user import user_companies
from schemas.company_schemas import CompanyCreate, CompanyUpdate
from services.role_manager import RoleManager, get_role_manager
from sqlalchemy.orm import Session
from fastapi import Depends


from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from data.session import db_session
from data.models.company import Company
from data.models.user import User, user_companies
from schemas.company_schemas import CompanyCreate, CompanyUpdate
from services.role_manager import RoleManager, get_role_manager
from sqlalchemy.orm import Session
from fastapi import Depends


class CompanyService:
    def __init__(self, db: Session, role_manager: RoleManager):
        self.db = db
        self.role_manager = role_manager

    def create_company(self, company_data: CompanyCreate, owner_firebase_uid: str) -> Company:
        try:
            owner = self.db.query(User).filter(User.firebase_uid == owner_firebase_uid).first()
            if not owner:
                raise ValueError("Власника компанії не знайдено")

            new_company = Company(
                name=company_data.name,
                description=company_data.description
            )
            self.db.add(new_company)
            self.db.flush()

            self.role_manager.assign_owner_role(owner_firebase_uid, new_company.id)

            self.db.commit()
            self.db.refresh(new_company)
            return new_company
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Компанія з такою назвою вже існує")

    def get_user_company(self, company_id: int, firebase_uid: str) -> Company:
        user = self.db.query(User).filter(User.firebase_uid == firebase_uid).first()
        if not user:
            raise ValueError("Користувача не знайдено")

        company = self.db.query(Company).join(user_companies).filter(
            Company.id == company_id,
            user_companies.c.user_id == user.id
        ).first()

        if not company:
            raise ValueError("Компанію не знайдено або у вас немає доступу до неї")

        return company

    def get_user_companies(self, firebase_uid: str) -> List[Company]:
        user = self.db.query(User).filter(User.firebase_uid == firebase_uid).first()
        if not user:
            raise ValueError("Користувача не знайдено")
        return self.db.query(Company).join(user_companies).filter(user_companies.c.user_id == user.id).all()

    def update_company(self, company_id: int, company_data: CompanyUpdate, firebase_uid: str) -> Company:
        company = self.get_user_company(company_id, firebase_uid)

        for key, value in company_data.dict(exclude_unset=True).items():
            setattr(company, key, value)

        try:
            self.db.commit()
            self.db.refresh(company)
            return company
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Компанія з такою назвою вже існує")

    def delete_company(self, company_id: int, firebase_uid: str) -> dict:
        company = self.get_user_company(company_id, firebase_uid)
        self.db.delete(company)
        self.db.commit()
        return {"message": "Компанію успішно видалено"}

    def get_company_users(self, company_id: int, firebase_uid: str):
        self.get_user_company(company_id, firebase_uid)
        return self.db.query(user_companies).filter(
            user_companies.c.company_id == company_id
        ).all()

    def add_user_to_company(self, company_id: int, email: str, role_id: int, firebase_uid: str):
        self.get_user_company(company_id, firebase_uid)
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError("Користувача не знайдено")

        exists = self.db.query(user_companies).filter(
            user_companies.c.company_id == company_id,
            user_companies.c.user_id == user.id
        ).first()

        if exists:
            raise ValueError("Користувач вже є у цій компанії")

        try:
            self.role_manager.assign_role(user.id, role_id, company_id)
            return {"message": "Користувача успішно додано до компанії"}
        except ValueError as e:
            raise ValueError(str(e))

    def remove_user_from_company(self, company_id: int, email: str, firebase_uid: str):
        self.get_user_company(company_id, firebase_uid)
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError("Користувача не знайдено")
        result = self.db.query(user_companies).filter(
            user_companies.c.company_id == company_id,
            user_companies.c.user_id == user.id
        ).delete()
        self.db.commit()
        if result:
            return {"message": "Користувача успішно видалено з компанії"}
        else:
            raise ValueError("Користувача не знайдено в цій компанії")


def get_company_manager(
    db: Session = Depends(db_session),
    role_manager: RoleManager = Depends(get_role_manager)
) -> CompanyService:
    return CompanyService(db, role_manager)