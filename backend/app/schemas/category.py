from pydantic import BaseModel
from typing import Optional


class CategoryTranslationCreate(BaseModel):
    locale: str
    name:   str


class CategoryTranslationOut(CategoryTranslationCreate):
    id: int

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    code_prefix:  str
    sort_order:   int = 0
    translations: list[CategoryTranslationCreate] = []


class CategoryUpdate(BaseModel):
    code_prefix:   Optional[str] = None
    product_count: Optional[int] = None
    sort_order:    Optional[int] = None


class CategoryOut(BaseModel):
    id:            int
    code_prefix:   str
    product_count: int
    sort_order:    int
    translations:  list[CategoryTranslationOut] = []

    class Config:
        from_attributes = True
