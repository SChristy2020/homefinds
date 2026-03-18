from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class ZelleRefund(str, Enum):
    phone = "phone"
    email = "email"
    other = "other"

class UserCreate(BaseModel):
    first_name:         str
    last_name:          str
    salutation:         str
    email:              EmailStr
    phone:              str
    zelle_refund:       ZelleRefund = ZelleRefund.phone
    zelle_refund_other: Optional[str] = None
    has_reservation:    int = 0
    has_purchase:       int = 0
    locale:             str = "zh-TW"

class UserOut(UserCreate):
    id:              int
    has_purchase:    int
    has_reservation: int
    is_admin:        int
    created_at:      datetime

    class Config:
        from_attributes = True
