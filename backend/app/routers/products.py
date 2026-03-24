from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel as PydanticModel
import threading
from app.database import get_db, SessionLocal
from app.models.product import Product, ProductTranslation, ProductImage
from app.models.category import Category, CategoryTranslation
from app.models.order import Order, OrderItem
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut, ImageOut, TranslationCreate, TranslationOut
from app.services.email_service import (
    send_product_restored_notification,
    send_item_snatched_pending_notification,
    send_order_auto_cancelled_notification,
)

class SortItem(PydanticModel):
    id: int
    sort_order: int

router = APIRouter()

def _build_out(product, db):
    translations = db.query(ProductTranslation).filter(ProductTranslation.product_id == product.id).all()
    images = db.query(ProductImage).filter(ProductImage.product_id == product.id).order_by(ProductImage.sort_order).all()
    out = ProductOut.model_validate(product)
    out.translations = translations
    out.images = images
    return out

@router.get("", response_model=list[ProductOut])
def list_products(visible_only: bool = False, db: Session = Depends(get_db)):
    q = db.query(Product)
    if visible_only:
        q = q.filter(Product.is_visible == True)
    products = q.all()
    return [_build_out(p, db) for p in products]

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return _build_out(product, db)

@router.post("", response_model=ProductOut, status_code=201)
def create_product(body: ProductCreate, db: Session = Depends(get_db)):
    data = body.model_dump(exclude={"translations"})
    product = Product(**data)
    db.add(product)
    db.flush()
    for t in body.translations:
        db.add(ProductTranslation(product_id=product.id, **t.model_dump()))
    cat_translation = db.query(CategoryTranslation).filter(
        CategoryTranslation.locale == 'en',
        CategoryTranslation.name == body.category
    ).first()
    if cat_translation:
        category = db.query(Category).filter(Category.id == cat_translation.category_id).first()
        if category:
            category.product_count += 1
    db.commit()
    db.refresh(product)
    return _build_out(product, db)

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, body: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if body.category is not None and body.category != product.category:
        old_cat_trans = db.query(CategoryTranslation).filter(
            CategoryTranslation.locale == 'en',
            CategoryTranslation.name == product.category
        ).first()
        if old_cat_trans:
            old_cat = db.query(Category).filter(Category.id == old_cat_trans.category_id).first()
            if old_cat and old_cat.product_count > 0:
                old_cat.product_count -= 1
        new_cat_trans = db.query(CategoryTranslation).filter(
            CategoryTranslation.locale == 'en',
            CategoryTranslation.name == body.category
        ).first()
        if new_cat_trans:
            new_cat = db.query(Category).filter(Category.id == new_cat_trans.category_id).first()
            if new_cat:
                new_cat.product_count += 1
    old_status = product.status
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(product, field, value)
    new_status = product.status

    # 商品從 available/reserved 改成 sold：連鎖更新未付款訂單
    _snatched_affected_ids: set[int] = set()
    _snatched_cancelled_ids: set[int] = set()
    if old_status in ("available", "reserved") and new_status == "sold":
        _snatched_affected_ids, _snatched_cancelled_ids = _handle_product_sold(product_id, db)

    # 商品從 sold 改回 available/reserved：連鎖更新相關訂單
    trigger_restore_email = False
    if old_status == "sold" and new_status in ("available", "reserved"):
        _handle_product_unsold(product_id, db)
        trigger_restore_email = True

    db.commit()
    db.refresh(product)

    # 寄信通知所有受搶購影響的訂單 user
    if _snatched_affected_ids:
        _pid = product_id
        _affected = set(_snatched_affected_ids)
        _cancelled = set(_snatched_cancelled_ids)

        def _send_snatched_emails():
            new_db = SessionLocal()
            try:
                for affected_order_id in _affected:
                    try:
                        affected_order = new_db.query(Order).filter(Order.id == affected_order_id).first()
                        if not affected_order:
                            continue
                        affected_user = new_db.query(User).filter(User.id == affected_order.user_id).first()
                        if not affected_user:
                            continue
                        if affected_order_id in _cancelled:
                            send_order_auto_cancelled_notification(
                                affected_user, affected_order.order_number, [_pid], new_db
                            )
                        else:
                            send_item_snatched_pending_notification(
                                affected_user, [_pid], new_db
                            )
                    except Exception as e:
                        print(f"[update_product sold] affected order {affected_order_id} email failed: {e}")
            finally:
                new_db.close()

        threading.Thread(target=_send_snatched_emails, daemon=True).start()

    if trigger_restore_email:
        _pid = product_id
        def _send_restore_emails():
            new_db = SessionLocal()
            try:
                sent_user_ids = set()
                # 通知任何狀態且含該商品的訂單購買者
                all_items = new_db.query(OrderItem).filter(
                    OrderItem.product_id == _pid,
                ).all()
                for oi in all_items:
                    order = new_db.query(Order).filter(Order.id == oi.order_id).first()
                    if not order:
                        continue
                    user = new_db.query(User).filter(User.id == order.user_id).first()
                    if not user or user.id in sent_user_ids:
                        continue
                    sent_user_ids.add(user.id)
                    send_product_restored_notification(user, [_pid], new_db)
            finally:
                new_db.close()
        threading.Thread(target=_send_restore_emails, daemon=True).start()

    return _build_out(product, db)


def _handle_product_sold(product_id: int, db: Session) -> tuple[set[int], set[int]]:
    """Admin 直接將商品設為 sold 時，連鎖更新所有未付款訂單中的該商品項目。
    回傳 (affected_order_ids, cancelled_order_ids)。"""
    from datetime import datetime
    sold_at = datetime.now()

    # 找出所有「未付款」訂單中狀態為 reserved 的該商品項目
    pending_items = (
        db.query(OrderItem)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(
            OrderItem.product_id == product_id,
            OrderItem.status == "reserved",
            Order.order_status == "pending_payment",
        )
        .all()
    )

    affected_order_ids: set[int] = set()
    for item in pending_items:
        item.status = "sold"
        item.sold_at = sold_at
        affected_order_ids.add(item.order_id)

    db.flush()

    # 若某訂單所有商品都已售出或取消 → 自動取消該訂單
    cancelled_order_ids: set[int] = set()
    for order_id in affected_order_ids:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order or order.order_status != "pending_payment":
            continue
        all_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        if all_items and all(i.status in ("sold", "cancelled") for i in all_items):
            order.order_status = "cancelled"
            cancelled_order_ids.add(order_id)

    return affected_order_ids, cancelled_order_ids


def _handle_product_unsold(product_id: int, db: Session):
    """商品從 sold 改回 available/reserved 時，處理相關訂單的連鎖更新。"""

    # 1. 已付款訂單：item.status="paid"（搶購成功）→ 改回 "reserved"（原本順位）
    #    不更新訂單物品數量和訂單總額，該商品 row 保留灰色背景
    paid_items = (
        db.query(OrderItem)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(
            OrderItem.product_id == product_id,
            OrderItem.status == "paid",
            Order.order_status == "paid",
        )
        .all()
    )
    for item in paid_items:
        item.status = "reserved"
        item.sold_at = None

    # 2. 未付款訂單：item.status="sold" → "reserved"
    #    取消灰色背景，改回目前順位，刪除出售日期
    pending_items = (
        db.query(OrderItem)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(
            OrderItem.product_id == product_id,
            OrderItem.status == "sold",
            Order.order_status == "pending_payment",
        )
        .all()
    )
    for item in pending_items:
        item.status = "reserved"
        item.sold_at = None

    # 3. 已取消訂單：item.status="sold" → "reserved"
    #    取消灰色背景，改回目前順位，刪除出售日期
    #    訂單 row 取消灰色背景，訂單狀態改成 pending_payment
    cancelled_items = (
        db.query(OrderItem)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(
            OrderItem.product_id == product_id,
            OrderItem.status == "sold",
            Order.order_status == "cancelled",
        )
        .all()
    )
    restored_order_ids = set()
    for item in cancelled_items:
        item.status = "reserved"
        item.sold_at = None
        restored_order_ids.add(item.order_id)

    for oid in restored_order_ids:
        order = db.query(Order).filter(Order.id == oid).first()
        if order:
            order.order_status = "pending_payment"

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()

@router.put("/{product_id}/translations/{locale}", response_model=TranslationOut)
def upsert_product_translation(product_id: int, locale: str, body: TranslationCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    translation = db.query(ProductTranslation).filter(
        ProductTranslation.product_id == product_id,
        ProductTranslation.locale == locale
    ).first()
    if translation:
        for field, value in body.model_dump(exclude_none=True, exclude={"locale"}).items():
            setattr(translation, field, value)
    else:
        translation = ProductTranslation(product_id=product_id, **body.model_dump())
        db.add(translation)
    db.commit()
    db.refresh(translation)
    return translation

@router.post("/{product_id}/images", response_model=ImageOut, status_code=201)
def add_image(product_id: int, url: str, sort_order: int = 0, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    image = ProductImage(product_id=product_id, url=url, sort_order=sort_order)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

@router.delete("/{product_id}/images/{image_id}", status_code=204)
def delete_product_image(product_id: int, image_id: int, db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(ProductImage.id == image_id, ProductImage.product_id == product_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    db.commit()

@router.put("/{product_id}/images/reorder", status_code=200)
def reorder_product_images(product_id: int, body: List[SortItem], db: Session = Depends(get_db)):
    for item in body:
        image = db.query(ProductImage).filter(ProductImage.id == item.id, ProductImage.product_id == product_id).first()
        if image:
            image.sort_order = item.sort_order
    db.commit()
    return {"ok": True}

@router.get("/{product_id}/waiting-list")
def get_waiting_list(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.waiting_list_summary or []
