from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.models.user import User
from app.services.email_service import send_pickup_reminder_notification


def send_due_pickup_reminders(db: Session, now: datetime | None = None) -> dict:
    now = now or datetime.now()
    cutoff = now + timedelta(hours=24)

    due_orders = (
        db.query(Order)
        .filter(
            Order.order_status.in_(("pending_payment", "paid")),
            Order.pickup_time.isnot(None),
            Order.pickup_time > now,
            Order.pickup_time <= cutoff,
            Order.pickup_reminder_sent_at.is_(None),
        )
        .all()
    )

    sent = 0
    skipped = 0
    failed = 0

    for order in due_orders:
        user = db.query(User).filter(User.id == order.user_id).first()
        if not user:
            skipped += 1
            continue

        product_rows = (
            db.query(OrderItem.product_id)
            .filter(
                OrderItem.order_id == order.id,
                OrderItem.status.in_(("paid", "reserved")),
            )
            .all()
        )
        product_ids = [row[0] for row in product_rows]
        if not product_ids:
            skipped += 1
            continue

        db.refresh(order)
        if order.order_status not in ("pending_payment", "paid"):
            skipped += 1
            continue

        try:
            send_pickup_reminder_notification(
                user=user,
                order_number=order.order_number,
                pickup_time=order.pickup_time,
                product_ids=product_ids,
                db=db,
            )
            order.pickup_reminder_sent_at = datetime.now()
            db.commit()
            sent += 1
        except Exception as e:
            db.rollback()
            failed += 1
            print(f"[pickup_reminder] order_id={order.id} send failed: {e}")

    return {
        "checked": len(due_orders),
        "sent": sent,
        "skipped": skipped,
        "failed": failed,
    }
