from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category, CategoryTranslation
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut

router = APIRouter()


def _build_out(category, db):
    translations = db.query(CategoryTranslation).filter(CategoryTranslation.category_id == category.id).all()
    out = CategoryOut.model_validate(category)
    out.translations = translations
    return out


@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return [_build_out(c, db) for c in categories]


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return _build_out(category, db)


@router.post("", response_model=CategoryOut, status_code=201)
def create_category(body: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(code_prefix=body.code_prefix)
    db.add(category)
    db.flush()
    for t in body.translations:
        db.add(CategoryTranslation(category_id=category.id, **t.model_dump()))
    db.commit()
    db.refresh(category)
    return _build_out(category, db)


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, body: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return _build_out(category, db)


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
