from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

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
    cancelled_at:     Optional[datetime]
    sold_at:          Optional[datetime]
    updated_at:       datetime
    waiting_position: Optional[int] = None
    product_name:     Optional[str] = None
    original_price:   Optional[float] = None
    image_url:        Optional[str] = None
    available_time:   Optional[datetime] = None

    class Config:
        from_attributes = True

class OrderPickupTimeUpdate(BaseModel):
    pickup_time: Optional[datetime] = None

class OrderCreate(BaseModel):
    user_id:     int
    pickup_time: Optional[datetime] = None
    items:       list[OrderItemCreate]
    locale:      str = "zh-TW"

class OrderOut(BaseModel):
    id:           int
    order_number: Optional[str]
    user_id:      int
    order_status: str
    paid_at:     Optional[datetime]
    pickup_time: Optional[datetime]
    created_at:  datetime
    updated_at:  datetime
    items:       list[OrderItemOut] = []
    buyer_first_name: Optional[str] = None
    buyer_last_name:  Optional[str] = None
    buyer_email:      Optional[str] = None
    buyer_phone:      Optional[str] = None

    class Config:
        from_attributes = True
