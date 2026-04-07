from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    role = Column(ForeignKey('users_roles.role_id'), default=1)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String(255), nullable=False)
    cart = relationship("Cart", back_populates="user")

class Role(Base):
    __tablename__ = 'users_roles'

    role_id = Column(Integer, primary_key=True)
    name = Column(String(50))