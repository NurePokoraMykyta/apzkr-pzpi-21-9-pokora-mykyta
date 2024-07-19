from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from data.session import Base
from .role import role_permissions

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")