import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, Table, ForeignKey, func, Float
from sqlalchemy.orm import relationship

from data.session import Base


class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


user_companies = Table('user_companies', Base.metadata,
                       Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
                       Column('company_id', Integer, ForeignKey('companies.id'), primary_key=True),
                       Column('role_id', Integer, ForeignKey('roles.id'))
                       )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firebase_uid = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    companies = relationship("Company", secondary=user_companies, back_populates="users")
    notifications = relationship("Notification", back_populates="user")
