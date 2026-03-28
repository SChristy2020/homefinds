from pydantic import BaseModel
from typing import Optional, Any
from datetime import date, datetime
from enum import Enum

class ProductStatus(str, Enum):
    available = "available"
    reserved  = "reserved"
    sold      = "sold"

class TranslationCreate(BaseModel):
    locale:      str
    name:        str
    description: Optional[str] = None

class TranslationOut(TranslationCreate):
    id: int
    class Config:
        from_attributes = True

class ImageOut(BaseModel):
    id:         int
    url:        str
    name:       Optional[str] = None
    sort_order: int
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    code:                  str
    category:              str
    price:                 float
    original_price:        Optional[float] = None
    status:                ProductStatus = ProductStatus.available
    is_visible:            bool = False
    sort:                  int = 0
    pickup_available_time: Optional[datetime] = None
    listed_date:           date
    translations:          list[TranslationCreate] = []

class ProductUpdate(BaseModel):
    code:                  Optional[str] = None
    category:              Optional[str] = None
    price:                 Optional[float] = None
    original_price:        Optional[float] = None
    status:                Optional[ProductStatus] = None
    is_visible:            Optional[bool] = None
    sort:                  Optional[int] = None
    pickup_available_time: Optional[datetime] = None

class ProductOut(BaseModel):
    id:                    int
    code:                  str
    category:              str
    price:                 float
    original_price:        Optional[float]
    status:                str
    is_visible:            bool
    sort:                  int
    pickup_available_time: Optional[datetime]
    listed_date:           date
    waiting_list_summary:  Optional[Any]
    created_at:            datetime
    updated_at:            datetime
    translations:          list[TranslationOut] = []
    images:                list[ImageOut] = []

    class Config:
        from_attributes = True
