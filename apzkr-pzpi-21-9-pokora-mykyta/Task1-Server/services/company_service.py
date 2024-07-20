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

    def get_company(self, company_id: int) -> Company:
        company = self.db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise ValueError("Компанію не знайдено")
        return company

    def get_companies(self) -> List[Company]:
        return self.db.query(Company).all()

    def update_company(self, company_id: int, company_data: CompanyUpdate) -> Company:
        company = self.get_company(company_id)

        for key, value in company_data.dict(exclude_unset=True).items():
            setattr(company, key, value)

        try:
            self.db.commit()
            self.db.refresh(company)
            return company
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Компанія з такою назвою вже існує")

    def delete_company(self, company_id: int) -> dict:
        company = self.get_company(company_id)
        self.db.delete(company)
        self.db.commit()
        return {"message": "Компанію успішно видалено"}

    def get_company_users(self, company_id: int, skip: int = 0, limit: int = 100):
        company = self.get_company(company_id)
        return self.db.query(user_companies).filter(
            user_companies.c.company_id == company_id
        ).offset(skip).limit(limit).all()

    def add_user_to_company(self, company_id: int, user_firebase_uid: str, role_id: int):
        company = self.get_company(company_id)
        user = self.db.query(User).filter(User.firebase_uid == user_firebase_uid).first()
        if not user:
            raise ValueError("Користувача не знайдено")
        try:
            self.role_manager.assign_role(user.id, role_id, company_id)
            return {"message": "Користувача успішно додано до компанії"}
        except ValueError as e:
            raise ValueError(str(e))

    def remove_user_from_company(self, company_id: int, user_firebase_uid: str):
        company = self.get_company(company_id)
        user = self.db.query(User).filter(User.firebase_uid == user_firebase_uid).first()
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