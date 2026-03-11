from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.dialects.mysql import TINYINT
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id                 = Column(Integer, primary_key=True, autoincrement=True)
    first_name         = Column(String(50),  nullable=False)
    last_name          = Column(String(50),  nullable=False)
    salutation         = Column(String(10),  nullable=False)
    email              = Column(String(100), nullable=False)
    phone              = Column(String(20),  nullable=False)
    zelle_refund       = Column(Enum("phone", "email", "other"), nullable=False, default="phone")
    zelle_refund_other = Column(String(100), nullable=True)
    has_purchase       = Column(TINYINT(1), nullable=False, default=0)
    has_reservation    = Column(TINYINT(1), nullable=False, default=0)
    is_admin           = Column(TINYINT(1), nullable=False, default=0)
    created_at         = Column(DateTime, nullable=False, server_default=func.now())
