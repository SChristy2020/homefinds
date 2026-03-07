from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationOut

router = APIRouter()

@router.post("", response_model=ReservationOut, status_code=201)
def create_reservation(body: ReservationCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == body.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    reservation = Reservation(**body.model_dump())
    db.add(reservation)
    user.has_reservation = 1
    db.commit()
    db.refresh(reservation)
    return reservation

@router.get("/user/{user_id}", response_model=list[ReservationOut])
def get_reservations_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.user_id == user_id).all()

@router.get("/{reservation_id}", response_model=ReservationOut)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    r = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return r

@router.put("/{reservation_id}/deposit-paid", response_model=ReservationOut)
def mark_deposit_paid(reservation_id: int, db: Session = Depends(get_db)):
    r = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")
    r.deposit_paid = 1
    db.commit()
    db.refresh(r)
    return r

@router.put("/{reservation_id}/fully-paid", response_model=ReservationOut)
def mark_fully_paid(reservation_id: int, db: Session = Depends(get_db)):
    r = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")
    r.fully_paid = 1
    db.commit()
    db.refresh(r)
    return r
