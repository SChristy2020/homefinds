from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.waiting_list import WaitingList
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.waiting_list import WaitingListCreate, WaitingListOut

router = APIRouter()

@router.post("", response_model=WaitingListOut, status_code=201)
def join_waiting_list(body: WaitingListCreate, db: Session = Depends(get_db)):
    # 計算目前候補順位
    count = db.query(WaitingList).filter(
        WaitingList.product_id == body.product_id,
        WaitingList.is_cancelled == 0,
    ).count()
    entry = WaitingList(product_id=body.product_id, user_id=body.user_id, position=count + 1)
    db.add(entry)

    # 更新 product 的 waiting_list_summary
    _refresh_summary(body.product_id, db)

    db.commit()
    db.refresh(entry)
    return entry

@router.put("/{entry_id}/cancel", response_model=WaitingListOut)
def cancel_waiting(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(WaitingList).filter(WaitingList.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    entry.is_cancelled = 1
    _refresh_summary(entry.product_id, db)
    db.commit()
    db.refresh(entry)
    return entry

def _refresh_summary(product_id: int, db: Session):
    entries = db.query(WaitingList).filter(WaitingList.product_id == product_id).all()
    from app.models.user import User
    summary = []
    for e in entries:
        user = db.query(User).filter(User.id == e.user_id).first()

        # 若 is_cancelled=0，再確認該 user 是否仍有有效（非取消）的訂單，
        # 若無，自動修正為 is_cancelled=1 以修復舊資料不一致的問題
        if not e.is_cancelled:
            has_active_order = (
                db.query(OrderItem)
                .join(Order, OrderItem.order_id == Order.id)
                .filter(
                    Order.user_id == e.user_id,
                    OrderItem.product_id == product_id,
                    OrderItem.status != "cancelled",
                    Order.order_status != "cancelled",
                )
                .first() is not None
            )
            if not has_active_order:
                e.is_cancelled = 1

        summary.append({
            "user_id":      e.user_id,
            "last_name":    user.last_name if user else "",
            "email":        user.email if user else "",
            "phone":        user.phone if user else "",
            "position":     e.position,
            "is_cancelled": bool(e.is_cancelled),
        })
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.waiting_list_summary = summary
