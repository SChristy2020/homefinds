import threading
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationOut, ReservationWithUser
from app.services.email_service import (
    send_reservation_confirmation,
    send_deposit_notification,
    send_deposit_confirmed_notification,
    send_reservation_cancelled_overlap_notification,
    send_reservation_cancelled_by_admin_notification,
    send_pending_deposit_admin_reminder,
    send_dates_available_again_notification,
)

ORDER_STATUSES = ['待付訂金', '待入住', '已入住', '已退房', '已取消']
# 已確認訂金的狀態（這些時段不可被其他訂單選用）
CONFIRMED_STATUSES = {'待入住', '已入住'}

class OrderStatusUpdate(BaseModel):
    order_status: str

class AdminNoteUpdate(BaseModel):
    admin_note: str

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

    def _check_pending_after_1h():
        new_db = SessionLocal()
        try:
            res = new_db.query(Reservation).filter(Reservation.id == _reservation_id).first()
            if res and res.order_status == '待付訂金':
                send_pending_deposit_admin_reminder(res, new_db)
        finally:
            new_db.close()
    threading.Timer(3600, _check_pending_after_1h).start()
    # threading.Timer(3600, _check_pending_after_1h).start()

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
            buyer_zelle_refund=u.zelle_refund,
            buyer_zelle_refund_other=u.zelle_refund_other,
        )
        for r, u in rows
    ]

@router.get("/user/{user_id}", response_model=list[ReservationOut])
def get_reservations_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.user_id == user_id).all()

@router.get("/blocked-dates", response_model=List[dict])
def get_blocked_dates(db: Session = Depends(get_db)):
    """回傳已確認訂金的訂單時段（用於前端日曆封鎖）。"""
    confirmed = db.query(Reservation).filter(
        Reservation.order_status.in_(list(CONFIRMED_STATUSES))
    ).all()
    return [{"check_in": str(r.check_in), "check_out": str(r.check_out)} for r in confirmed]

@router.get("/{reservation_id}", response_model=ReservationOut)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    r = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return r

@router.post("/{reservation_id}/notify-deposit", status_code=200)
def notify_deposit_paid(reservation_id: int, db: Session = Depends(get_db)):
    r = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")
    user = db.query(User).filter(User.id == r.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    _user_id, _reservation_id = user.id, r.id
    def _send_email():
        new_db = SessionLocal()
        try:
            new_user = new_db.query(User).filter(User.id == _user_id).first()
            new_reservation = new_db.query(Reservation).filter(Reservation.id == _reservation_id).first()
            send_deposit_notification(new_user, new_reservation, new_db)
        finally:
            new_db.close()
    threading.Thread(target=_send_email, daemon=True).start()
    return {"ok": True}

@router.patch("/{reservation_id}/admin-note", response_model=ReservationOut)
def update_admin_note(reservation_id: int, body: AdminNoteUpdate, db: Session = Depends(get_db)):
    r = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")
    r.admin_note = body.admin_note
    db.commit()
    db.refresh(r)
    return r

@router.put("/{reservation_id}/status", response_model=ReservationOut)
def update_order_status(reservation_id: int, body: OrderStatusUpdate, db: Session = Depends(get_db)):
    if body.order_status not in ORDER_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid order_status. Must be one of: {ORDER_STATUSES}")
    r = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")

    old_status = r.order_status
    r.order_status = body.order_status
    db.commit()
    db.refresh(r)

    # 當 admin 將狀態改為「待入住」時，觸發特殊流程
    if body.order_status == '待入住' and old_status != '待入住':
        _handle_deposit_confirmed(r, db)

    # 當 admin 將狀態從「待付訂金」改為「已取消」時，通知 user
    if body.order_status == '已取消' and old_status == '待付訂金':
        _user_id, _reservation_id = r.user_id, r.id
        def _send_cancel_email():
            new_db = SessionLocal()
            try:
                new_user = new_db.query(User).filter(User.id == _user_id).first()
                new_reservation = new_db.query(Reservation).filter(Reservation.id == _reservation_id).first()
                if new_user and new_reservation:
                    send_reservation_cancelled_by_admin_notification(new_user, new_reservation, new_db)
            finally:
                new_db.close()
        threading.Thread(target=_send_cancel_email, daemon=True).start()

    # 當 admin 將狀態從「待入住」改為「已取消」時，通知 user 並通知時段重疊的已取消訂單 user
    if body.order_status == '已取消' and old_status == '待入住':
        _handle_checkin_status_cancelled(r, db)

    return r


def _handle_checkin_status_cancelled(cancelled_res: Reservation, db: Session):
    """處理「待入住」訂單被取消後的流程：通知該訂單 user、並通知其他時段重疊的已取消訂單 user。"""
    # 1. 通知被取消訂單的 user
    _cancelled_user_id = cancelled_res.user_id
    _cancelled_res_id = cancelled_res.id

    # 2. 找出所有時段完全包含在被取消時段內的其他已取消訂單
    overlapping_cancelled = db.query(Reservation).filter(
        Reservation.id != cancelled_res.id,
        Reservation.order_status == '已取消',
        Reservation.check_in >= cancelled_res.check_in,
        Reservation.check_out <= cancelled_res.check_out,
    ).all()
    overlap_pairs = [(res.user_id, res.id) for res in overlapping_cancelled]

    def _send_emails():
        new_db = SessionLocal()
        try:
            # 通知該訂單 user 訂單已取消
            cancelled_user = new_db.query(User).filter(User.id == _cancelled_user_id).first()
            cancelled_reservation = new_db.query(Reservation).filter(Reservation.id == _cancelled_res_id).first()
            if cancelled_user and cancelled_reservation:
                send_reservation_cancelled_by_admin_notification(cancelled_user, cancelled_reservation, new_db)

            # 通知時段重疊的已取消訂單 user：時段重新開放
            for user_id, res_id in overlap_pairs:
                overlap_user = new_db.query(User).filter(User.id == user_id).first()
                overlap_res = new_db.query(Reservation).filter(Reservation.id == res_id).first()
                if overlap_user and overlap_res:
                    send_dates_available_again_notification(overlap_user, overlap_res, new_db)
        finally:
            new_db.close()

    threading.Thread(target=_send_emails, daemon=True).start()


def _handle_deposit_confirmed(confirmed_res: Reservation, db: Session):
    """處理訂金確認後的流程：通知 user、取消時間重疊的訂單並通知那些 user。"""
    # 1. 找出所有時間重疊且未取消的其他訂單
    overlapping = db.query(Reservation).filter(
        Reservation.id != confirmed_res.id,
        Reservation.order_status != '已取消',
        Reservation.check_in < confirmed_res.check_out,
        Reservation.check_out > confirmed_res.check_in,
    ).all()

    # 2. 取消重疊訂單並收集需通知的 (user_id, reservation_id)
    cancelled_pairs = []
    for res in overlapping:
        res.order_status = '已取消'
        cancelled_pairs.append((res.user_id, res.id))
    if overlapping:
        db.commit()

    # 3. 在背景非同步寄信（確認通知 + 取消通知）
    _confirmed_user_id = confirmed_res.user_id
    _confirmed_res_id = confirmed_res.id

    def _send_emails():
        new_db = SessionLocal()
        try:
            # 寄「訂金已確認」給該訂單的 user
            conf_user = new_db.query(User).filter(User.id == _confirmed_user_id).first()
            conf_res = new_db.query(Reservation).filter(Reservation.id == _confirmed_res_id).first()
            if conf_user and conf_res:
                send_deposit_confirmed_notification(conf_user, conf_res, new_db)

            # 寄「時段被搶先，訂單取消」給每個被取消的 user
            for user_id, res_id in cancelled_pairs:
                cancelled_user = new_db.query(User).filter(User.id == user_id).first()
                cancelled_res = new_db.query(Reservation).filter(Reservation.id == res_id).first()
                if cancelled_user and cancelled_res:
                    send_reservation_cancelled_overlap_notification(cancelled_user, cancelled_res, new_db)
        finally:
            new_db.close()

    threading.Thread(target=_send_emails, daemon=True).start()
