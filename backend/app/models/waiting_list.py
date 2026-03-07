from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.mysql import TINYINT
from app.database import Base

class WaitingList(Base):
    __tablename__ = "waiting_list"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    product_id   = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"),  nullable=False)
    user_id      = Column(Integer, ForeignKey("users.id",    ondelete="RESTRICT"), nullable=False)
    position     = Column(Integer, nullable=False)
    is_cancelled = Column(TINYINT(1), nullable=False, default=0)
    created_at   = Column(DateTime, nullable=False, server_default=func.now())
