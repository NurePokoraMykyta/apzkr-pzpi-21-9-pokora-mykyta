from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data.session import Base


class IoTDevice(Base):
    __tablename__ = 'iot_devices'

    id = Column(Integer, primary_key=True)
    unique_address = Column(String, unique=True, nullable=False)
    aquarium_id = Column(Integer, ForeignKey('aquariums.id'), unique=True, nullable=False)

    aquarium = relationship("Aquarium", back_populates="iot_device")
    food_patches = relationship("FoodPatch", back_populates="iot_device")
