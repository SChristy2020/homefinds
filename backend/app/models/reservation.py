from sqlalchemy import Column, Integer, Numeric, Date, DateTime, ForeignKey, Text, String, func
from sqlalchemy.dialects.mysql import TINYINT
from app.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id                       = Column(Integer, primary_key=True, autoincrement=True)
    order_number             = Column(String(20),    nullable=True)
    user_id                  = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    check_in                 = Column(Date,          nullable=False)
    check_out                = Column(Date,          nullable=False)
    nights                   = Column(Integer,       nullable=False)
    deposit_paid             = Column(TINYINT(1),    nullable=False, default=0)
    deposit_amount           = Column(Numeric(10,2), nullable=False)
    total_price              = Column(Numeric(10,2), nullable=False)
    original_price           = Column(Numeric(10,2), nullable=True)
    special_price            = Column(Numeric(10,2), nullable=True)
    early_bird_price         = Column(Numeric(10,2), nullable=True)
    is_early_bird            = Column(TINYINT(1),    nullable=False, default=0)
    fully_paid               = Column(TINYINT(1),    nullable=False, default=0)
    birth_year               = Column(Integer,       nullable=True)
    occupation               = Column(String(100),   nullable=True)
    has_guests_or_pets       = Column(TINYINT(1),    nullable=False, default=0)
    guests_pets_description  = Column(Text,          nullable=True)
    special_requests         = Column(Text,          nullable=True)
    created_at               = Column(DateTime,      nullable=False, server_default=func.now())
    updated_at               = Column(DateTime,      nullable=False, server_default=func.now(), onupdate=func.now())
