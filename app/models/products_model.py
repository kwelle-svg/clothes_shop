from sqlalchemy import (Column, Integer, String,
                        Date, Numeric, ForeignKey)
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(250))
    brand_id = Column(ForeignKey("brands.brand_id"))
    category_id = Column(ForeignKey("categories.category_id"))
    created_at = Column(Date, default=date.today)
    price = Column(Numeric(10,2))
    sale = Column(Numeric(1,2), default=0)
    # img = Column()
    # quantity = Column(Integer)


class Brand(Base):
    __tablename__ = 'brands'

    brand_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(300))


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    user = relationship("User", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")