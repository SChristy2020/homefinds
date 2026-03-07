from sqlalchemy import Column, Integer, Numeric, Enum, DateTime, ForeignKey, func
from sqlalchemy.dialects.mysql import TINYINT
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    user_id     = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    is_paid     = Column(TINYINT(1), nullable=False, default=0)
    paid_at     = Column(DateTime, nullable=True)
    pickup_time = Column(DateTime, nullable=True)
    created_at  = Column(DateTime, nullable=False, server_default=func.now())
    updated_at  = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class OrderItem(Base):
    __tablename__ = "order_items"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    order_id     = Column(Integer, ForeignKey("orders.id",    ondelete="CASCADE"),  nullable=False)
    product_id   = Column(Integer, ForeignKey("products.id",  ondelete="RESTRICT"), nullable=False)
    price        = Column(Numeric(10, 2), nullable=False)
    status       = Column(Enum("reserved", "cancelled", "paid"), nullable=False, default="reserved")
    cancelled_at = Column(DateTime, nullable=True)
    updated_at   = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
