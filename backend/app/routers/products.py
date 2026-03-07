from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product, ProductTranslation, ProductImage
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut, ImageOut

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
    db.commit()
    db.refresh(product)
    return _build_out(product, db)

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, body: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return _build_out(product, db)

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

@router.get("/{product_id}/waiting-list")
def get_waiting_list(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.waiting_list_summary or []
