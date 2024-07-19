from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data.session import Base


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
