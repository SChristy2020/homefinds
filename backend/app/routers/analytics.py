from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from app.database import get_db
from app.models.product import Product
from app.models.user import User
from app.models.order import Order, OrderItem
from app.models.reservation import Reservation

router = APIRouter()


@router.get("")
def get_analytics(db: Session = Depends(get_db)):
    # ── Products ──────────────────────────────────────────────
    total_products = db.query(func.count(Product.id)).scalar() or 0
    sold_products  = db.query(func.count(Product.id)).filter(Product.status == "sold").scalar() or 0
    unsold_products = total_products - sold_products

    # ── Users by locale ───────────────────────────────────────
    locale_rows = (
        db.query(User.locale, func.count(User.id))
        .group_by(User.locale)
        .all()
    )
    users_by_locale = {row[0]: row[1] for row in locale_rows}

    # ── Shop orders by status ─────────────────────────────────
    shop_status_rows = (
        db.query(Order.order_status, func.count(Order.id))
        .group_by(Order.order_status)
        .all()
    )
    shop_orders_by_status = {row[0]: row[1] for row in shop_status_rows}

    # ── Rent orders by status ─────────────────────────────────
    rent_status_rows = (
        db.query(Reservation.order_status, func.count(Reservation.id))
        .group_by(Reservation.order_status)
        .all()
    )
    rent_orders_by_status = {row[0]: row[1] for row in rent_status_rows}

    # ── Shop orders daily (last 90 days) ──────────────────────
    shop_daily = _build_shop_daily(db)

    # ── Rent orders daily (last 90 days) ──────────────────────
    rent_daily = _build_rent_daily(db)

    return {
        "products": {
            "sold":   sold_products,
            "unsold": unsold_products,
            "total":  total_products,
        },
        "users_by_locale": users_by_locale,
        "shop_orders_by_status": shop_orders_by_status,
        "rent_orders_by_status": rent_orders_by_status,
        "shop_daily": shop_daily,
        "rent_daily": rent_daily,
    }


def _build_shop_daily(db: Session):
    """每日購物訂單數與金額（取 created_at 日期）。"""
    rows = (
        db.query(
            func.date(Order.created_at).label("day"),
            func.count(Order.id).label("count"),
        )
        .group_by(func.date(Order.created_at))
        .order_by(func.date(Order.created_at))
        .all()
    )

    # order amount = sum of item prices per order
    amount_rows = (
        db.query(
            func.date(Order.created_at).label("day"),
            func.sum(OrderItem.price).label("amount"),
        )
        .join(OrderItem, OrderItem.order_id == Order.id)
        .filter(OrderItem.status != "cancelled")
        .group_by(func.date(Order.created_at))
        .order_by(func.date(Order.created_at))
        .all()
    )
    amount_map = {str(r.day): float(r.amount) for r in amount_rows}

    labels, daily_count, daily_amount, cum_count, cum_amount = [], [], [], [], []
    c_sum, a_sum = 0, 0
    for r in rows:
        day_str = str(r.day)
        labels.append(day_str)
        daily_count.append(r.count)
        amt = amount_map.get(day_str, 0.0)
        daily_amount.append(amt)
        c_sum += r.count
        a_sum += amt
        cum_count.append(c_sum)
        cum_amount.append(round(a_sum, 2))

    return {"labels": labels, "daily_count": daily_count, "daily_amount": daily_amount,
            "cum_count": cum_count, "cum_amount": cum_amount}


def _build_rent_daily(db: Session):
    """每日租屋訂單數與金額（取 created_at 日期）。"""
    rows = (
        db.query(
            func.date(Reservation.created_at).label("day"),
            func.count(Reservation.id).label("count"),
            func.sum(Reservation.total_price).label("amount"),
        )
        .group_by(func.date(Reservation.created_at))
        .order_by(func.date(Reservation.created_at))
        .all()
    )

    labels, daily_count, daily_amount, cum_count, cum_amount = [], [], [], [], []
    c_sum, a_sum = 0, 0.0
    for r in rows:
        labels.append(str(r.day))
        daily_count.append(r.count)
        amt = float(r.amount) if r.amount else 0.0
        daily_amount.append(amt)
        c_sum += r.count
        a_sum += amt
        cum_count.append(c_sum)
        cum_amount.append(round(a_sum, 2))

    return {"labels": labels, "daily_count": daily_count, "daily_amount": daily_amount,
            "cum_count": cum_count, "cum_amount": cum_amount}
