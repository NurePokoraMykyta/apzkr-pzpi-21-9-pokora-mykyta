from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from data.session import Base


class FoodPatch(Base):
    __tablename__ = 'food_patches'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    food_type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)  # в граммах
    iot_device_id = Column(Integer, ForeignKey('iot_devices.id'), nullable=False)

    iot_device = relationship("IoTDevice", back_populates="food_patches")
