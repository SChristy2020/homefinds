from sqlalchemy import Column, Integer, String, Enum, Numeric, Date, DateTime, Text, JSON, Boolean, func, ForeignKey
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id                    = Column(Integer, primary_key=True, autoincrement=True)
    code                  = Column(String(50),  nullable=False, unique=True)
    category              = Column(String(50), nullable=False)
    price                 = Column(Numeric(10, 2), nullable=False)
    original_price        = Column(Numeric(10, 2), nullable=True)
    status                = Column(Enum("available", "reserved", "sold"), nullable=False, default="available")
    is_visible            = Column(Boolean, nullable=False, default=False)
    pickup_available_time = Column(DateTime, nullable=True)
    listed_date           = Column(Date, nullable=False)
    waiting_list_summary  = Column(JSON, nullable=True)
    created_at            = Column(DateTime, nullable=False, server_default=func.now())
    updated_at            = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class ProductTranslation(Base):
    __tablename__ = "product_translations"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    product_id  = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    locale      = Column(Enum("en", "zh-TW", "zh-CN"), nullable=False)
    name        = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)


class ProductImage(Base):
    __tablename__ = "product_images"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    url        = Column(String(500), nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
