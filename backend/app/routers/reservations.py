import threading
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationOut, ReservationWithUser
from app.services.email_service import send_reservation_confirmation

router = APIRouter()

@router.post("", response_model=ReservationOut, status_code=201)
def create_reservation(body: ReservationCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == body.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    reservation = Reservation(**body.model_dump())
    db.add(reservation)
    user.has_reservation = 1
    db.flush()  # get reservation.id before commit
    dep = str(int(reservation.deposit_amount)).zfill(3)
    nts = str(reservation.nights).zfill(2)
    reservation.order_number = f"R{str(reservation.id).zfill(2)}{dep}{nts}"
    db.commit()
    db.refresh(reservation)

    _user_id, _reservation_id = user.id, reservation.id
    def _send_email():
        new_db = SessionLocal()
        try:
            new_user = new_db.query(User).filter(User.id == _user_id).first()
            new_reservation = new_db.query(Reservation).filter(Reservation.id == _reservation_id).first()
            send_reservation_confirmation(new_user, new_reservation, new_db)
        finally:
            new_db.close()
    threading.Thread(target=_send_email, daemon=True).start()

    return reservation

@router.get("/all", response_model=list[ReservationWithUser])
def get_all_reservations(db: Session = Depends(get_db)):
    rows = db.query(Reservation, User).join(User, Reservation.user_id == User.id).order_by(Reservation.id.desc()).all()
    return [
        ReservationWithUser(
            **{c.key: getattr(r, c.key) for c in Reservation.__table__.columns},
            buyer_first_name=u.first_name,
            buyer_last_name=u.last_name,
            buyer_email=u.email,
            buyer_phone=u.phone,
            buyer_salutation=u.salutation,
        )
        for r, u in rows
    ]

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

@router.put("/{reservation_id}/deposit-unpaid", response_model=ReservationOut)
def mark_deposit_unpaid(reservation_id: int, db: Session = Depends(get_db)):
    r = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")
    r.deposit_paid = 0
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

@router.put("/{reservation_id}/fully-unpaid", response_model=ReservationOut)
def mark_fully_unpaid(reservation_id: int, db: Session = Depends(get_db)):
    r = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")
    r.fully_paid = 0
    db.commit()
    db.refresh(r)
    return r
