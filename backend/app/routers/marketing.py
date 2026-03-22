from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.product import Product
from app.services.email_service import send_marketing_email

router = APIRouter()


class MarketingSendRequest(BaseModel):
    product_ids: List[int]
    admin_id: int


@router.post("/send")
def send_marketing(body: MarketingSendRequest, db: Session = Depends(get_db)):
    admin = db.query(User).filter(User.id == body.admin_id, User.is_admin == 1).first()
    if not admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    subscribers = db.query(User).filter(User.is_subscribed_marketing == 1).all()
    if not subscribers:
        return {"sent": 0, "message": "No subscribers found"}

    sent = 0
    for user in subscribers:
        try:
            send_marketing_email(user, body.product_ids, db)
            sent += 1
        except Exception as e:
            print(f"Failed to send marketing email to {user.email}: {e}")

    return {"sent": sent}
