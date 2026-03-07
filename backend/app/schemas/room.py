from pydantic import BaseModel
from typing import Optional
from datetime import date

class RoomUpdate(BaseModel):
    available_from:    Optional[date]  = None
    available_to:      Optional[date]  = None
    price_per_night:   Optional[float] = None
    price_7_nights:    Optional[float] = None
    price_30_days:     Optional[float] = None
    price_full_period: Optional[float] = None
    description:       Optional[str]   = None

class RoomImageOut(BaseModel):
    id:         int
    url:        str
    sort_order: int
    class Config:
        from_attributes = True

class RoomOut(BaseModel):
    id:                int
    available_from:    date
    available_to:      date
    price_per_night:   float
    price_7_nights:    Optional[float]
    price_30_days:     Optional[float]
    price_full_period: Optional[float]
    description:       Optional[str]
    images:            list[RoomImageOut] = []

    class Config:
        from_attributes = True
