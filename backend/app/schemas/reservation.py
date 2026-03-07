from pydantic import BaseModel
from datetime import date, datetime

class ReservationCreate(BaseModel):
    user_id:        int
    check_in:       date
    check_out:      date
    nights:         int
    deposit_amount: float
    total_price:    float

class ReservationOut(BaseModel):
    id:             int
    user_id:        int
    check_in:       date
    check_out:      date
    nights:         int
    deposit_paid:   int
    deposit_amount: float
    total_price:    float
    fully_paid:     int
    created_at:     datetime
    updated_at:     datetime

    class Config:
        from_attributes = True
