from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel as PydanticModel
from app.database import get_db
from app.models.product import Product, ProductTranslation, ProductImage
from app.models.category import Category, CategoryTranslation
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut, ImageOut, TranslationCreate, TranslationOut

class SortItem(PydanticModel):
    id: int
    sort_order: int

router = APIRouter()

def _build_out(product, db):
    translations = db.query(ProductTranslation).filter(ProductTranslation.product_id == product.id).all()
    images = db.query(ProductImage).filter(ProductImage.product_id == product.id).order_by(ProductImage.sort_order).all()
    out = ProductOut.model_validate(product)
    out.translations = translations
    out.images = images
    return out

@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [_build_out(p, db) for p in products]

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return _build_out(product, db)

@router.post("", response_model=ProductOut, status_code=201)
def create_product(body: ProductCreate, db: Session = Depends(get_db)):
    data = body.model_dump(exclude={"translations"})
    product = Product(**data)
    db.add(product)
    db.flush()
    for t in body.translations:
        db.add(ProductTranslation(product_id=product.id, **t.model_dump()))
    cat_translation = db.query(CategoryTranslation).filter(
        CategoryTranslation.locale == 'en',
        CategoryTranslation.name == body.category
    ).first()
    if cat_translation:
        category = db.query(Category).filter(Category.id == cat_translation.category_id).first()
        if category:
            category.product_count += 1
    db.commit()
    db.refresh(product)
    return _build_out(product, db)

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, body: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if body.category is not None and body.category != product.category:
        old_cat_trans = db.query(CategoryTranslation).filter(
            CategoryTranslation.locale == 'en',
            CategoryTranslation.name == product.category
        ).first()
        if old_cat_trans:
            old_cat = db.query(Category).filter(Category.id == old_cat_trans.category_id).first()
            if old_cat and old_cat.product_count > 0:
                old_cat.product_count -= 1
        new_cat_trans = db.query(CategoryTranslation).filter(
            CategoryTranslation.locale == 'en',
            CategoryTranslation.name == body.category
        ).first()
        if new_cat_trans:
            new_cat = db.query(Category).filter(Category.id == new_cat_trans.category_id).first()
            if new_cat:
                new_cat.product_count += 1
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return _build_out(product, db)

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()

@router.put("/{product_id}/translations/{locale}", response_model=TranslationOut)
def upsert_product_translation(product_id: int, locale: str, body: TranslationCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    translation = db.query(ProductTranslation).filter(
        ProductTranslation.product_id == product_id,
        ProductTranslation.locale == locale
    ).first()
    if translation:
        for field, value in body.model_dump(exclude_none=True, exclude={"locale"}).items():
            setattr(translation, field, value)
    else:
        translation = ProductTranslation(product_id=product_id, **body.model_dump())
        db.add(translation)
    db.commit()
    db.refresh(translation)
    return translation

@router.post("/{product_id}/images", response_model=ImageOut, status_code=201)
def add_image(product_id: int, url: str, sort_order: int = 0, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    image = ProductImage(product_id=product_id, url=url, sort_order=sort_order)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

@router.delete("/{product_id}/images/{image_id}", status_code=204)
def delete_product_image(product_id: int, image_id: int, db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(ProductImage.id == image_id, ProductImage.product_id == product_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    db.commit()

@router.put("/{product_id}/images/reorder", status_code=200)
def reorder_product_images(product_id: int, body: List[SortItem], db: Session = Depends(get_db)):
    for item in body:
        image = db.query(ProductImage).filter(ProductImage.id == item.id, ProductImage.product_id == product_id).first()
        if image:
            image.sort_order = item.sort_order
    db.commit()
    return {"ok": True}

@router.get("/{product_id}/waiting-list")
def get_waiting_list(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.waiting_list_summary or []
