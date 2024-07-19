import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, Table, ForeignKey, func, Float
from sqlalchemy.orm import relationship

from data.session import Base


class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class NotificationType(enum.Enum):
    FEEDING = "feeding"
    WATER_QUALITY = "water_quality"
    MAINTENANCE = "maintenance"


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(NotificationType), nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User")


user_companies = Table('user_companies', Base.metadata,
                       Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
                       Column('company_id', Integer, ForeignKey('companies.id'), primary_key=True),
                       Column('role_id', Integer, ForeignKey('roles.id'))
                       )

role_permissions = Table('role_permissions', Base.metadata,
                         Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
                         Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
                         )


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User", secondary="user_companies")


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


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    users = relationship("User", secondary=user_companies, back_populates="companies")
    aquariums = relationship("Aquarium", back_populates="company")


class WaterParameter(Base):
    __tablename__ = 'water_parameters'

    id = Column(Integer, primary_key=True)
    ph = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    salinity = Column(Float, nullable=False)
    oxygen_level = Column(Float, nullable=False)
    measured_at = Column(DateTime, nullable=False)
    aquarium_id = Column(Integer, ForeignKey('aquariums.id'), nullable=False)

    aquarium = relationship("Aquarium", back_populates="water_parameters")


class Fish(Base):
    __tablename__ = 'fish'

    id = Column(Integer, primary_key=True)
    species = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    aquarium_id = Column(Integer, ForeignKey('aquariums.id'), nullable=False)

    aquarium = relationship("Aquarium", back_populates="fish")


class FoodPatch(Base):
    __tablename__ = 'food_patches'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    food_type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)  # в граммах
    iot_device_id = Column(Integer, ForeignKey('iot_devices.id'), nullable=False)

    iot_device = relationship("IoTDevice", back_populates="food_patches")


class IoTDevice(Base):
    __tablename__ = 'iot_devices'

    id = Column(Integer, primary_key=True)
    unique_address = Column(String, unique=True, nullable=False)
    aquarium_id = Column(Integer, ForeignKey('aquariums.id'), unique=True, nullable=False)

    aquarium = relationship("Aquarium", back_populates="iot_device")
    food_patches = relationship("FoodPatch", back_populates="iot_device")


class FeedingSchedule(Base):
    __tablename__ = 'feeding_schedules'

    id = Column(Integer, primary_key=True)
    food_type = Column(String, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    aquarium_id = Column(Integer, ForeignKey('aquariums.id'), nullable=False)

    aquarium = relationship("Aquarium", back_populates="feeding_schedules")


class Aquarium(Base):
    __tablename__ = 'aquariums'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    capacity = Column(Float, nullable=False)  # в литрах
    description = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)

    company = relationship("Company", back_populates="aquariums")
    feeding_schedules = relationship("FeedingSchedule", back_populates="aquarium")
    water_parameters = relationship("WaterParameter", back_populates="aquarium")
    fish = relationship("Fish", back_populates="aquarium")
    iot_device = relationship("IoTDevice", back_populates="aquarium", uselist=False)
