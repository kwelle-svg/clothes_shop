from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from datetime import datetime
from app.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(250))
    brand_id = Column(ForeignKey("brands.brand_id"))
    category_id = Column(ForeignKey("categories.category_id"))
    created_at = Column(Date, default=datetime.now("%Y-%m-%d"))
    price = Column(Numeric(10,2))
    sale = Column(Numeric(1,2), default=0)


class Brand(Base):
    __tablename__ = 'brands'

    brand_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(300))