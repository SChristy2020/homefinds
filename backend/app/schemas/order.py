from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
from app.schemas import UTCDatetime

class ItemStatus(str, Enum):
    reserved  = "reserved"
    cancelled = "cancelled"
    paid      = "paid"
    sold      = "sold"

class OrderItemCreate(BaseModel):
    product_id: int
    price:      float

class OrderItemOut(BaseModel):
    id:               int
    product_id:       int
    price:            float
    status:           str
    cancelled_at:     Optional[UTCDatetime]
    sold_at:          Optional[UTCDatetime]
    updated_at:       UTCDatetime
    waiting_position: Optional[int] = None
    product_name:     Optional[str] = None
    original_price:   Optional[float] = None
    image_url:        Optional[str] = None
    available_time:   Optional[UTCDatetime] = None

    class Config:
        from_attributes = True

class OrderPickupTimeUpdate(BaseModel):
    pickup_time: Optional[datetime] = None

class RevertPaidBody(BaseModel):
    target_status: str  # "pending_payment" or "cancelled"

class OrderCreate(BaseModel):
    user_id:     int
    pickup_time: Optional[datetime] = None
    items:       list[OrderItemCreate]
    locale:      str = "zh-TW"

class AdminNotesUpdate(BaseModel):
    admin_notes: Optional[str] = None

class OrderOut(BaseModel):
    id:           int
    order_number: Optional[str]
    user_id:      int
    order_status: str
    paid_at:     Optional[UTCDatetime]
    pickup_time: Optional[UTCDatetime]
    created_at:  UTCDatetime
    updated_at:  UTCDatetime
    items:       list[OrderItemOut] = []
    buyer_first_name:        Optional[str] = None
    buyer_last_name:         Optional[str] = None
    buyer_email:             Optional[str] = None
    buyer_phone:             Optional[str] = None
    buyer_zelle_refund:      Optional[str] = None
    buyer_zelle_refund_other: Optional[str] = None
    admin_notes:             Optional[str] = None

    class Config:
        from_attributes = True
