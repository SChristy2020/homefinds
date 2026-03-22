from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut

router = APIRouter()

@router.post("", response_model=UserOut)
def create_user(body: UserCreate, response: Response, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        User.last_name.ilike(body.last_name),
        User.email.ilike(body.email),
        User.phone == body.phone,
    ).first()

    if existing:
        existing.first_name        = body.first_name
        existing.salutation        = body.salutation
        existing.zelle_refund      = body.zelle_refund
        existing.zelle_refund_other = body.zelle_refund_other
        if body.has_reservation:
            existing.has_reservation = 1
        if body.has_purchase:
            existing.has_purchase = 1
        if body.is_subscribed_marketing:
            existing.is_subscribed_marketing = 1
        db.commit()
        db.refresh(existing)
        response.status_code = 200
        return existing

    data = body.model_dump(exclude={"locale"})
    user = User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    response.status_code = 201
    return user

@router.get("/lookup", response_model=UserOut)
def lookup_user(last_name: str, email: str, phone: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.last_name.ilike(last_name),
        User.email.ilike(email),
        User.phone == phone,
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
