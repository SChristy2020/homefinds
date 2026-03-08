from sqlalchemy import Column, Integer, Numeric, Date, Text, String, Enum, ForeignKey
from app.database import Base

class Room(Base):
    __tablename__ = "room"

    id                = Column(Integer, primary_key=True, autoincrement=True)
    available_from    = Column(Date,          nullable=False)
    available_to      = Column(Date,          nullable=False)
    price_per_night   = Column(Numeric(10,2), nullable=False)
    price_7_nights    = Column(Numeric(10,2), nullable=True)
    price_30_days     = Column(Numeric(10,2), nullable=True)
    price_full_period = Column(Numeric(10,2), nullable=True)


class RoomTranslation(Base):
    __tablename__ = "room_translations"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    room_id             = Column(Integer, ForeignKey("room.id", ondelete="CASCADE"), nullable=False)
    locale              = Column(Enum("en", "zh-TW", "zh-CN"), nullable=False)
    description         = Column(Text, nullable=True)
    booking_description = Column(Text, nullable=True)


class RoomImage(Base):
    __tablename__ = "room_images"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    room_id    = Column(Integer, ForeignKey("room.id", ondelete="CASCADE"), nullable=False)
    url        = Column(String(500), nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
