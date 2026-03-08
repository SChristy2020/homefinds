from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List
from pydantic import BaseModel as PydanticModel
from app.database import get_db
from app.models.room import Room, RoomImage, RoomTranslation
from app.models.reservation import Reservation
from app.schemas.room import RoomUpdate, RoomOut, RoomImageOut, RoomTranslationCreate, RoomTranslationOut

class SortItem(PydanticModel):
    id: int
    sort_order: int

router = APIRouter()

def _build_out(room, db):
    translations = db.query(RoomTranslation).filter(RoomTranslation.room_id == room.id).all()
    images = db.query(RoomImage).filter(RoomImage.room_id == room.id).order_by(RoomImage.sort_order).all()
    out = RoomOut.model_validate(room)
    out.translations = translations
    out.images = images
    return out

@router.get("", response_model=list[RoomOut])
def list_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    return [_build_out(r, db) for r in rooms]

@router.get("/availability")
def get_availability(db: Session = Depends(get_db)):
    """回傳所有已出租的日期區間"""
    reservations = db.query(Reservation).all()
    return [{"check_in": str(r.check_in), "check_out": str(r.check_out)} for r in reservations]

@router.put("/{room_id}", response_model=RoomOut)
def update_room(room_id: int, body: RoomUpdate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(room, field, value)
    db.commit()
    db.refresh(room)
    return _build_out(room, db)

@router.put("/{room_id}/translations/{locale}", response_model=RoomTranslationOut)
def upsert_room_translation(room_id: int, locale: str, body: RoomTranslationCreate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    translation = db.query(RoomTranslation).filter(
        RoomTranslation.room_id == room_id,
        RoomTranslation.locale == locale
    ).first()
    if translation:
        for field, value in body.model_dump(exclude_none=True, exclude={"locale"}).items():
            setattr(translation, field, value)
    else:
        translation = RoomTranslation(room_id=room_id, **body.model_dump())
        db.add(translation)
    db.commit()
    db.refresh(translation)
    return translation


@router.post("/{room_id}/images", response_model=RoomImageOut, status_code=201)
def add_room_image(room_id: int, url: str, sort_order: int = 0, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    image = RoomImage(room_id=room_id, url=url, sort_order=sort_order)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

@router.delete("/{room_id}/images/{image_id}", status_code=204)
def delete_room_image(room_id: int, image_id: int, db: Session = Depends(get_db)):
    image = db.query(RoomImage).filter(RoomImage.id == image_id, RoomImage.room_id == room_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    db.commit()

@router.put("/{room_id}/images/reorder", status_code=200)
def reorder_room_images(room_id: int, body: List[SortItem], db: Session = Depends(get_db)):
    for item in body:
        image = db.query(RoomImage).filter(RoomImage.id == item.id, RoomImage.room_id == room_id).first()
        if image:
            image.sort_order = item.sort_order
    db.commit()
    return {"ok": True}
