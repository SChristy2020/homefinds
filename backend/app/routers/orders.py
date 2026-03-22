from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import threading
from app.database import get_db, SessionLocal
from app.models.order import Order, OrderItem
from app.models.product import Product, ProductTranslation, ProductImage
from app.models.user import User
from app.models.waiting_list import WaitingList
from app.schemas.order import OrderCreate, OrderOut, OrderItemOut, OrderPickupTimeUpdate, RevertPaidBody, AdminNotesUpdate
from app.routers.waiting_list import _refresh_summary
from app.services.email_service import (
    send_order_confirmation,
    send_product_restored_notification,
    send_payment_success_notification,
    send_item_snatched_pending_notification,
    send_order_auto_cancelled_notification,
    send_order_status_reverted_notification,
)

router = APIRouter()

def _build_out(order, db):
    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    out = OrderOut.model_validate(order)
    user = db.query(User).filter(User.id == order.user_id).first()
    if user:
        out.buyer_first_name        = user.first_name
        out.buyer_last_name         = user.last_name
        out.buyer_email             = user.email
        out.buyer_phone             = user.phone
        out.buyer_zelle_refund      = user.zelle_refund
        out.buyer_zelle_refund_other = user.zelle_refund_other
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

        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            item_out.original_price = float(product.original_price) if product.original_price else None
            item_out.available_time = product.pickup_available_time
            translation = db.query(ProductTranslation).filter(
                ProductTranslation.product_id == item.product_id,
                ProductTranslation.locale == "zh-TW",
            ).first()
            if translation:
                item_out.product_name = translation.name
            image = db.query(ProductImage).filter(
                ProductImage.product_id == item.product_id,
            ).order_by(ProductImage.sort_order).first()
            if image:
                item_out.image_url = image.url

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

    short_id = str(order.id)[-6:]
    total    = int(sum(item.price for item in body.items))
    count    = str(len(body.items)).zfill(2)
    order.order_number = f'S{short_id}{total}{count}'

    user.has_purchase = 1
    db.commit()
    db.refresh(order)
    order_out = _build_out(order, db)
    _user_id = user.id
    def _send_email():
        new_db = SessionLocal()
        try:
            new_user = new_db.query(User).filter(User.id == _user_id).first()
            send_order_confirmation(new_user, order_out, new_db)
        finally:
            new_db.close()

    threading.Thread(target=_send_email, daemon=True).start()
    return order_out

@router.get("/all", response_model=list[OrderOut])
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).order_by(Order.id.desc()).all()
    return [_build_out(o, db) for o in orders]

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
    order.order_status = "paid"
    order.paid_at = datetime.now()

    sold_at = datetime.now()

    # Mark each reserved item in this order as paid and cascade sold status
    paid_items = db.query(OrderItem).filter(
        OrderItem.order_id == order_id,
        OrderItem.status == "reserved",
    ).all()

    paid_product_ids = [item.product_id for item in paid_items]

    # Track which product_ids were snatched from each affected order
    snatched_by_order: dict[int, list[int]] = {}

    for item in paid_items:
        item.status = "paid"

        # Mark the product as sold
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.status = "sold"

        # Mark all other reserved order items for this product as sold
        other_items = db.query(OrderItem).filter(
            OrderItem.product_id == item.product_id,
            OrderItem.order_id != order_id,
            OrderItem.status == "reserved",
        ).all()
        for other_item in other_items:
            other_item.status = "sold"
            other_item.sold_at = sold_at
            snatched_by_order.setdefault(other_item.order_id, []).append(item.product_id)

    db.flush()

    # Auto-cancel orders where all items are now sold or cancelled
    cancelled_order_ids: set[int] = set()
    for affected_id in snatched_by_order:
        affected_order = db.query(Order).filter(Order.id == affected_id).first()
        if not affected_order or affected_order.order_status != "pending_payment":
            continue
        all_items = db.query(OrderItem).filter(OrderItem.order_id == affected_id).all()
        if all_items and all(i.status in ("sold", "cancelled") for i in all_items):
            affected_order.order_status = "cancelled"
            cancelled_order_ids.add(affected_id)

    db.commit()
    db.refresh(order)

    # Send emails asynchronously
    _paid_order_number = order.order_number
    _paid_pickup_time = order.pickup_time
    _paid_user_id = order.user_id
    _snatched_by_order = {oid: list(pids) for oid, pids in snatched_by_order.items()}
    _cancelled_order_ids = set(cancelled_order_ids)
    _paid_product_ids = list(paid_product_ids)

    def _send_paid_emails():
        new_db = SessionLocal()
        try:
            # 1. 寄信給付款成功的 user
            try:
                paid_user = new_db.query(User).filter(User.id == _paid_user_id).first()
                if paid_user:
                    send_payment_success_notification(
                        paid_user, _paid_order_number, _paid_pickup_time, _paid_product_ids, new_db
                    )
            except Exception as e:
                print(f"[mark_order_paid] payment success email failed: {e}")

            # 2 & 3. 寄信給受影響的訂單 user
            for affected_order_id, snatched_pids in _snatched_by_order.items():
                try:
                    affected_order = new_db.query(Order).filter(Order.id == affected_order_id).first()
                    if not affected_order:
                        continue
                    affected_user = new_db.query(User).filter(User.id == affected_order.user_id).first()
                    if not affected_user:
                        continue
                    if affected_order_id in _cancelled_order_ids:
                        # 訂單中所有商品皆被售出 → 訂單已自動取消
                        send_order_auto_cancelled_notification(
                            affected_user, affected_order.order_number, snatched_pids, new_db
                        )
                    else:
                        # 訂單中還有未售出商品 → 提醒盡速付款
                        send_item_snatched_pending_notification(
                            affected_user, snatched_pids, new_db
                        )
                except Exception as e:
                    print(f"[mark_order_paid] affected order {affected_order_id} email failed: {e}")
        finally:
            new_db.close()

    threading.Thread(target=_send_paid_emails, daemon=True).start()

    return _build_out(order, db)

@router.put("/{order_id}/revert-paid", response_model=OrderOut)
def revert_paid_order(order_id: int, body: RevertPaidBody, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.order_status != "paid":
        raise HTTPException(status_code=400, detail="Order is not paid")

    # 1. 找出此訂單中狀態為 "paid" 的物品（搶購成功的商品）
    paid_items = db.query(OrderItem).filter(
        OrderItem.order_id == order_id,
        OrderItem.status == "paid",
    ).all()
    affected_product_ids = [item.product_id for item in paid_items]

    # 2. 將此訂單的 paid 物品改回 reserved，商品狀態改回 available
    for item in paid_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.status = "available"
        item.status = "reserved"
        item.sold_at = None

    db.flush()

    # 3. 找出其他訂單中因此付款而被標記為 sold 的物品，改回 reserved
    cancelled_order_ids = set()
    for product_id in affected_product_ids:
        other_sold_items = db.query(OrderItem).filter(
            OrderItem.product_id == product_id,
            OrderItem.order_id != order_id,
            OrderItem.status == "sold",
        ).all()
        for other_item in other_sold_items:
            other_item.status = "reserved"
            other_item.sold_at = None
            other_order = db.query(Order).filter(Order.id == other_item.order_id).first()
            if other_order and other_order.order_status == "cancelled":
                cancelled_order_ids.add(other_item.order_id)

    db.flush()

    # 4. 將因自動取消而變成 cancelled 的訂單改回 pending_payment
    for affected_id in cancelled_order_ids:
        affected_order = db.query(Order).filter(Order.id == affected_id).first()
        if affected_order:
            affected_order.order_status = "pending_payment"

    # 5. 更新此訂單狀態
    order.order_status = body.target_status
    order.paid_at = None

    db.commit()
    db.refresh(order)

    # 6. 寄信通知所有含此商品的訂單購買者（非 cancelled 物品）
    _product_ids = affected_product_ids[:]
    _reverted_order_user_id = order.user_id
    _reverted_order_number = order.order_number
    _reverted_target_status = body.target_status

    def _send_restore_emails():
        new_db = SessionLocal()
        try:
            # 6a. 寄信給被 revert 的訂單 user，通知訂單狀態已變更
            try:
                reverted_user = new_db.query(User).filter(User.id == _reverted_order_user_id).first()
                if reverted_user:
                    send_order_status_reverted_notification(
                        reverted_user, _reverted_order_number, _reverted_target_status, _product_ids, new_db
                    )
            except Exception as e:
                print(f"[revert_paid_order] status reverted email failed: {e}")

            # 6b. 寄信通知所有含此商品的訂單購買者（非 cancelled 物品）商品已恢復
            sent_user_ids = set()
            items_for_products = new_db.query(OrderItem).filter(
                OrderItem.product_id.in_(_product_ids),
                OrderItem.status != "cancelled",
            ).all()
            for oi in items_for_products:
                ao = new_db.query(Order).filter(Order.id == oi.order_id).first()
                if not ao:
                    continue
                user = new_db.query(User).filter(User.id == ao.user_id).first()
                if not user or user.id in sent_user_ids:
                    continue
                sent_user_ids.add(user.id)
                send_product_restored_notification(user, _product_ids, new_db)
        finally:
            new_db.close()

    threading.Thread(target=_send_restore_emails, daemon=True).start()

    return _build_out(order, db)

@router.put("/{order_id}/picked_up", response_model=OrderOut)
def mark_order_picked_up(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.order_status = "picked_up"
    db.commit()
    db.refresh(order)
    return _build_out(order, db)

@router.put("/{order_id}/unpaid", response_model=OrderOut)
def mark_order_unpaid(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.order_status = "pending_payment"
    order.paid_at = None
    db.commit()
    db.refresh(order)
    return _build_out(order, db)

@router.put("/{order_id}/cancelled", response_model=OrderOut)
def mark_order_cancelled(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.order_status = "cancelled"
    order.paid_at = None
    db.commit()
    db.refresh(order)
    return _build_out(order, db)

@router.put("/{order_id}/pickup_time", response_model=OrderOut)
def update_pickup_time(order_id: int, body: OrderPickupTimeUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.pickup_time = body.pickup_time
    db.commit()
    db.refresh(order)
    return _build_out(order, db)

@router.put("/{order_id}/admin-notes", response_model=OrderOut)
def update_admin_notes(order_id: int, body: AdminNotesUpdate, admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(User).filter(User.id == admin_id, User.is_admin == 1).first()
    if not admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.admin_notes = body.admin_notes
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
