from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ReservationCreate(BaseModel):
    user_id:                 int
    check_in:                date
    check_out:               date
    nights:                  int
    deposit_amount:          float
    total_price:             float
    birth_year:              Optional[int] = None
    occupation:              Optional[str] = None
    has_guests_or_pets:      bool = False
    guests_pets_description: Optional[str] = None
    special_requests:        Optional[str] = None

class ReservationOut(BaseModel):
    id:                      int
    order_number:            Optional[str]
    user_id:                 int
    check_in:                date
    check_out:               date
    nights:                  int
    deposit_paid:            int
    deposit_amount:          float
    total_price:             float
    fully_paid:              int
    birth_year:              Optional[int]
    occupation:              Optional[str]
    has_guests_or_pets:      int
    guests_pets_description: Optional[str]
    special_requests:        Optional[str]
    created_at:              datetime
    updated_at:              datetime

    class Config:
        from_attributes = True

class ReservationWithUser(ReservationOut):
    buyer_first_name: str
    buyer_last_name:  str
    buyer_email:      str
    buyer_phone:      str
