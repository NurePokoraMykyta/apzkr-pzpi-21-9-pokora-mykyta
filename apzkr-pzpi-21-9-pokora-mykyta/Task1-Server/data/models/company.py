from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from data.session import Base
from .user import user_companies


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    users = relationship("User", secondary=user_companies, back_populates="companies")
    aquariums = relationship("Aquarium", back_populates="company")
