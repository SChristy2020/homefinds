r'''
Author: Christy qsa8647332@gmail.com
Date: 2026-03-21 23:04:45
LastEditors: Christy qsa8647332@gmail.com
LastEditTime: 2026-03-21 23:18:09
FilePath: \homefinds\backend\app\schemas\user.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class ZelleRefund(str, Enum):
    phone = "phone"
    email = "email"
    other = "other"

class UserCreate(BaseModel):
    first_name:              str
    last_name:               str
    salutation:              str
    email:                   EmailStr
    phone:                   str
    zelle_refund:            ZelleRefund = ZelleRefund.phone
    zelle_refund_other:      Optional[str] = None
    has_reservation:         int = 0
    has_purchase:            int = 0
    is_subscribed_marketing: int = 1
    locale:                  str = "zh-TW"

class UserOut(UserCreate):
    id:                      int
    has_purchase:            int
    has_reservation:         int
    is_admin:                int
    is_subscribed_marketing: int
    created_at:              datetime

    class Config:
        from_attributes = True
