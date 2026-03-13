from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ItemStatus(str, Enum):
    reserved  = "reserved"
    cancelled = "cancelled"
    paid      = "paid"

class OrderItemCreate(BaseModel):
    product_id: int
    price:      float

class OrderItemOut(BaseModel):
    id:               int
    product_id:       int
    price:            float
    status:           str
    cancelled_at:     Optional[datetime]
    updated_at:       datetime
    waiting_position: Optional[int] = None

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id:     int
    pickup_time: Optional[datetime] = None
    items:       list[OrderItemCreate]
    locale:      str = "zh-TW"

class OrderOut(BaseModel):
    id:          int
    user_id:     int
    is_paid:     int
    paid_at:     Optional[datetime]
    pickup_time: Optional[datetime]
    created_at:  datetime
    updated_at:  datetime
    items:       list[OrderItemOut] = []

    class Config:
        from_attributes = True
