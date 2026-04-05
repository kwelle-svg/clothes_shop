from sqlalchemy import Column, ForeignKey, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(250))
    role = Column(ForeignKey('users_roles.role_id'), default=1)

class Role(Base):
    __tablename__ = 'users_roles'

    role_id = Column(Integer, primary_key=True)
    name = Column(String(50))