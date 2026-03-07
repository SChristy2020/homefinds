from sqlalchemy import Column, Integer, Numeric, Date, DateTime, ForeignKey, func
from sqlalchemy.dialects.mysql import TINYINT
from app.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    user_id        = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    check_in       = Column(Date,          nullable=False)
    check_out      = Column(Date,          nullable=False)
    nights         = Column(Integer,       nullable=False)
    deposit_paid   = Column(TINYINT(1),    nullable=False, default=0)
    deposit_amount = Column(Numeric(10,2), nullable=False)
    total_price    = Column(Numeric(10,2), nullable=False)
    fully_paid     = Column(TINYINT(1),    nullable=False, default=0)
    created_at     = Column(DateTime,      nullable=False, server_default=func.now())
    updated_at     = Column(DateTime,      nullable=False, server_default=func.now(), onupdate=func.now())
