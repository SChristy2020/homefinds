from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import threading
from app.database import get_db, SessionLocal
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.waiting_list import WaitingList
from app.schemas.order import OrderCreate, OrderOut, OrderItemOut
from app.routers.waiting_list import _refresh_summary
from app.services.email_service import send_order_confirmation

router = APIRouter()

def _build_out(order, db):
    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    out = OrderOut.model_validate(order)
    enriched = []
    for item in items:
        position = (
            db.query(OrderItem)
            .join(Order, OrderItem.order_id == Order.id)
            .filter(
                OrderItem.product_id == item.product_id,
                OrderItem.status != "cancelled",
                Order.created_at <= order.created_at,
            )
            .count()
        )
        item_out = OrderItemOut.model_validate(item)
        item_out.waiting_position = position
        enriched.append(item_out)
    out.items = enriched
    return out

@router.post("", response_model=OrderOut, status_code=201)
def create_order(body: OrderCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == body.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check for duplicate reservations (same user already has active order for these products)
    duplicate_product_ids = []
    for item in body.items:
        existing = (
            db.query(OrderItem)
            .join(Order, OrderItem.order_id == Order.id)
            .filter(
                Order.user_id == user.id,
                OrderItem.product_id == item.product_id,
                OrderItem.status != "cancelled",
            )
            .first()
        )
        if existing:
            duplicate_product_ids.append(item.product_id)

    if duplicate_product_ids:
        raise HTTPException(
            status_code=409,
            detail={"duplicate_product_ids": duplicate_product_ids},
        )

    order = Order(user_id=body.user_id, pickup_time=body.pickup_time)
    db.add(order)
    db.flush()

    for item in body.items:
        db.add(OrderItem(order_id=order.id, product_id=item.product_id, price=item.price))
        position = db.query(WaitingList).filter(
            WaitingList.product_id == item.product_id,
            WaitingList.is_cancelled == 0,
        ).count() + 1
        db.add(WaitingList(product_id=item.product_id, user_id=body.user_id, position=position))

    db.flush()

    for item in body.items:
        _refresh_summary(item.product_id, db)

    user.has_reservation = 1
    db.commit()
    db.refresh(order)
    order_out = _build_out(order, db)
    def _send_email():
        new_db = SessionLocal()
        try:
            send_order_confirmation(user, order_out, new_db, locale=body.locale)
        finally:
            new_db.close()

    threading.Thread(target=_send_email, daemon=True).start()
    return order_out

@router.get("/user/{user_id}", response_model=list[OrderOut])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return [_build_out(o, db) for o in orders]

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _build_out(order, db)

@router.put("/{order_id}/paid", response_model=OrderOut)
def mark_order_paid(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.is_paid = 1
    order.paid_at = datetime.now()
    db.commit()
    db.refresh(order)
    return _build_out(order, db)

@router.put("/items/{item_id}/cancel", response_model=dict)
def cancel_order_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    item.status = "cancelled"
    item.cancelled_at = datetime.now()

    wl_entry = db.query(WaitingList).filter(
        WaitingList.product_id == item.product_id,
        WaitingList.user_id == db.query(Order.user_id).filter(Order.id == item.order_id).scalar_subquery(),
        WaitingList.is_cancelled == 0,
    ).first()
    if wl_entry:
        wl_entry.is_cancelled = 1
        _refresh_summary(item.product_id, db)

    db.commit()
    return {"message": "Item cancelled"}
