from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data.session import Base


class Fish(Base):
    __tablename__ = 'fish'

    id = Column(Integer, primary_key=True)
    species = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    aquarium_id = Column(Integer, ForeignKey('aquariums.id'), nullable=False)

    aquarium = relationship("Aquarium", back_populates="fish")
