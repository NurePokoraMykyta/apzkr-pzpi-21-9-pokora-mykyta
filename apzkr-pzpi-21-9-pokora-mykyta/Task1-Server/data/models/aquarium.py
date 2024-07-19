from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from data.session import Base


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
