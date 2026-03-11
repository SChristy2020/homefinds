from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut

router = APIRouter()

@router.post("", response_model=UserOut, status_code=201)
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    user = User(**body.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
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
