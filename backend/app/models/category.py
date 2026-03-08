from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    code_prefix   = Column(String(10), nullable=False, unique=True)
    product_count = Column(Integer, nullable=False, default=0)
    sort_order    = Column(Integer, nullable=False, default=0)


class CategoryTranslation(Base):
    __tablename__ = "category_translations"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    locale      = Column(Enum("en", "zh-TW", "zh-CN"), nullable=False)
    name        = Column(String(100), nullable=False)
