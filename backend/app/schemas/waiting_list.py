from pydantic import BaseModel
from datetime import datetime

class WaitingListCreate(BaseModel):
    product_id: int
    user_id:    int

class WaitingListOut(BaseModel):
    id:           int
    product_id:   int
    user_id:      int
    position:     int
    is_cancelled: int
    created_at:   datetime

    class Config:
        from_attributes = True
