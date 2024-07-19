from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from data.session import Base

role_permissions = Table('role_permissions', Base.metadata,
                         Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
                         Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
                         )


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User", secondary="user_companies")
