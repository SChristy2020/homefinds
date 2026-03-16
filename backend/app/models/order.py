from sqlalchemy import Column, Integer, Numeric, Enum, DateTime, ForeignKey, String, Text, func
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(String(20), unique=True, nullable=True)
    user_id      = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    order_status = Column(Enum("pending_payment", "paid", "cancelled"), nullable=False, default="pending_payment")
    paid_at      = Column(DateTime, nullable=True)
    pickup_time  = Column(DateTime, nullable=True)
    admin_notes  = Column(Text, nullable=True)
    created_at   = Column(DateTime, nullable=False, server_default=func.now())
    updated_at   = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class OrderItem(Base):
    __tablename__ = "order_items"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    order_id     = Column(Integer, ForeignKey("orders.id",    ondelete="CASCADE"),  nullable=False)
    product_id   = Column(Integer, ForeignKey("products.id",  ondelete="RESTRICT"), nullable=False)
    price        = Column(Numeric(10, 2), nullable=False)
    status       = Column(Enum("reserved", "cancelled", "paid", "sold"), nullable=False, default="reserved")
    cancelled_at = Column(DateTime, nullable=True)
    sold_at      = Column(DateTime, nullable=True)
    updated_at   = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
