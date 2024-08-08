from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from data import Aquarium, Fish, Role
from data.session import db_session
from data.models.company import Company
from data.models.user import user_companies
from schemas.aquarium_schemas import AquariumCreate, AquariumUpdate
from schemas.company_schemas import CompanyCreate, CompanyUpdate
from schemas.fish_schemas import FishCreate, FishUpdate
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
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
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

    def get_all_company_users(self, company_id: int):
        company = self.db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise ValueError(f"Компанія з ID {company_id} не знайдена")

        users_with_roles = self.db.query(User).join(user_companies).options(
            joinedload(User.companies).joinedload(Company.roles)
        ).filter(
            user_companies.c.company_id == company_id
        ).all()

        if not users_with_roles:
            return []

        return users_with_roles

    def add_user_to_company(self, company_id: int, email: str, role_id: int):
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

    def create_aquarium(self, company_id: int, aquarium_data: AquariumCreate, owner_firebase_uid: str) -> Aquarium:
        try:
            company = self.get_user_company(company_id, owner_firebase_uid)
        except ValueError as e:
            raise ValueError(f"Помилка при отриманні компанії: {str(e)}")

        new_aquarium = Aquarium(
            name=aquarium_data.name,
            capacity=aquarium_data.capacity,
            description=aquarium_data.description,
            company_id=company.id,
            created_at=func.now(),
            updated_at=func.now()
        )

        try:
            self.db.add(new_aquarium)
            self.db.commit()
            self.db.refresh(new_aquarium)
            return new_aquarium
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Акваріум з такою назвою вже існує в даній компанії")
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Помилка при створенні акваріума: {str(e)}")

    def get_company_aquariums(self, company_id: int, firebase_uid: str) -> List[Aquarium]:
        try:
            company = self.get_user_company(company_id, firebase_uid)
        except ValueError as e:
            raise ValueError(f"Помилка при отриманні компанії: {str(e)}")

        return self.db.query(Aquarium).options(
            joinedload(Aquarium.company),
            joinedload(Aquarium.feeding_schedules),
            joinedload(Aquarium.water_parameters),
            joinedload(Aquarium.fish),
            joinedload(Aquarium.iot_device)
        ).filter(Aquarium.company_id == company.id).all()

    def get_company_aquarium(self, company_id: int, aquarium_id: int, firebase_uid: str) -> Aquarium:
        try:
            company = self.get_user_company(company_id, firebase_uid)
        except ValueError as e:
            raise ValueError(f"Помилка при отриманні компанії: {str(e)}")

        aquarium = self.db.query(Aquarium).options(
            joinedload(Aquarium.feeding_schedules),
            joinedload(Aquarium.water_parameters),
            joinedload(Aquarium.fish),
            joinedload(Aquarium.iot_device)
        ).filter(Aquarium.id == aquarium_id, Aquarium.company_id == company.id).first()

        if not aquarium:
            raise ValueError("Акваріум не знайдено в зазначеній компанії")

        return aquarium

    def update_company_aquarium(self, company_id: int, aquarium_id: int, aquarium_data: AquariumUpdate,
                                firebase_uid: str) -> Aquarium:
        try:
            aquarium = self.get_company_aquarium(company_id, aquarium_id, firebase_uid)
        except ValueError as e:
            raise ValueError(f"Помилка при отриманні акваріума: {str(e)}")

        for key, value in aquarium_data.dict(exclude_unset=True).items():
            setattr(aquarium, key, value)

        try:
            self.db.commit()
            self.db.refresh(aquarium)
            return aquarium
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Акваріум з такою назвою вже існує в даній компанії")
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Помилка при оновленні акваріума: {str(e)}")

    def delete_company_aquarium(self, company_id: int, aquarium_id: int, firebase_uid: str) -> dict:
        try:
            aquarium = self.get_company_aquarium(company_id, aquarium_id, firebase_uid)
        except ValueError as e:
            raise ValueError(f"Помилка при отриманні акваріума: {str(e)}")

        try:
            self.db.delete(aquarium)
            self.db.commit()
            return {"message": "Акваріум успішно видалено"}
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Помилка при видаленні акваріума: {str(e)}")

    def add_fish_to_aquarium(self, fish_data: FishCreate, aquarium_id: int,  firebase_uid: str) -> Fish:
        aquarium = self.get_company_aquarium(fish_data.company_id, aquarium_id, firebase_uid)

        existing_fish = self.db.query(Fish).filter(
            Fish.aquarium_id == aquarium.id,
            Fish.species == fish_data.species
        ).first()

        if existing_fish:
            existing_fish.quantity += fish_data.quantity
            self.db.commit()
            self.db.refresh(existing_fish)
            return existing_fish
        else:
            new_fish = Fish(species=fish_data.species, quantity=fish_data.quantity, aquarium_id=aquarium.id)
            self.db.add(new_fish)
            self.db.commit()
            self.db.refresh(new_fish)
            return new_fish

    def get_aquarium_fish(self, company_id: int, aquarium_id: int, firebase_uid: str) -> List[Fish]:
        aquarium = self.db.query(Aquarium).filter(Aquarium.id == aquarium_id).first()
        if not aquarium:
            raise ValueError("Акваріум не знайдено")

        self.get_user_company(aquarium.company_id, firebase_uid)
        return self.db.query(Fish).filter(Fish.aquarium_id == aquarium.id).all()

    def get_fish(self, company_id: int, aquarium_id: int, fish_id: int, firebase_uid: str) -> Fish:
        aquarium = self.db.query(Aquarium).filter(Aquarium.id == aquarium_id).first()
        if not aquarium:
            raise ValueError("Акваріум не знайдено")

        self.get_user_company(aquarium.company_id, firebase_uid)
        fish = self.db.query(Fish).filter(Fish.id == fish_id, Fish.aquarium_id == aquarium.id).first()
        if not fish:
            raise ValueError("Рибу не знайдено")
        return fish

    def update_fish(self, company_id: int, aquarium_id: int, fish_id: int, fish_data: FishUpdate,
                    firebase_uid: str) -> Fish:
        fish = self.get_fish(company_id, aquarium_id, fish_id, firebase_uid)

        if fish_data.quantity is not None:
            if fish_data.quantity > 0:
                fish.quantity = fish_data.quantity
            elif fish_data.quantity == 0:
                self.db.delete(fish)
                self.db.commit()
                return None
            else:
                raise ValueError("Кількість риб не може бути від'ємною")

        if fish_data.species:
            fish.species = fish_data.species

        self.db.commit()
        self.db.refresh(fish)
        return fish

    def remove_fish(self, company_id: int, aquarium_id: int, fish_id: int, quantity: Optional[int],
                    firebase_uid: str) -> dict:
        fish = self.get_fish(company_id, aquarium_id, fish_id, firebase_uid)

        if quantity is None or quantity >= fish.quantity:
            self.db.delete(fish)
            message = "Рибу повністю видалено з акваріума"
        else:
            if quantity <= 0:
                raise ValueError("Кількість риб для видалення повинна бути більше нуля")
            fish.quantity -= quantity
            message = f"Кількість риб зменшено на {quantity}"

        self.db.commit()
        return {"message": message}


def get_company_manager(
    db: Session = Depends(db_session),
    role_manager: RoleManager = Depends(get_role_manager)
) -> CompanyService:
    return CompanyService(db, role_manager)