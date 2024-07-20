from sqlalchemy import Column, Integer, String, Table, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from data.session import Base


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    permissions = Column(ARRAY(String), default=[])
