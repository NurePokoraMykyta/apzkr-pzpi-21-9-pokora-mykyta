from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data.session import Base


class FeedingSchedule(Base):
    __tablename__ = 'feeding_schedules'

    id = Column(Integer, primary_key=True)
    food_type = Column(String, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    aquarium_id = Column(Integer, ForeignKey('aquariums.id'), nullable=False)

    aquarium = relationship("Aquarium", back_populates="feeding_schedules")
