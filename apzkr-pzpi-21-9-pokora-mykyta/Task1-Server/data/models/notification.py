import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from data.session import Base


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

    user = relationship("User", back_populates="notifications")
