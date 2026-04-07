from pydantic import BaseModel
from datetime import datetime
from app.schemas import UTCNaiveDatetime

class WaitingListCreate(BaseModel):
    product_id: int
    user_id:    int

class WaitingListOut(BaseModel):
    id:           int
    product_id:   int
    user_id:      int
    position:     int
    is_cancelled: int
    created_at:   UTCNaiveDatetime

    class Config:
        from_attributes = True
