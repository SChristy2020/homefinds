r'''
Author: Christy qsa8647332@gmail.com
Date: 2026-03-21 23:04:34
LastEditors: Christy qsa8647332@gmail.com
LastEditTime: 2026-03-21 23:17:22
FilePath: \homefinds\backend\app\models\user.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.dialects.mysql import TINYINT
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id                 = Column(Integer, primary_key=True, autoincrement=True)
    first_name         = Column(String(50),  nullable=False)
    last_name          = Column(String(50),  nullable=False)
    salutation         = Column(String(10),  nullable=False)
    email              = Column(String(100), nullable=False)
    phone              = Column(String(20),  nullable=False)
    zelle_refund       = Column(Enum("phone", "email", "other"), nullable=False, default="phone")
    zelle_refund_other = Column(String(100), nullable=True)
    locale             = Column(String(10),  nullable=False, default="zh-TW")
    has_purchase            = Column(TINYINT(1), nullable=False, default=0)
    has_reservation         = Column(TINYINT(1), nullable=False, default=0)
    is_admin                = Column(TINYINT(1), nullable=False, default=0)
    is_subscribed_marketing = Column(TINYINT(1), nullable=False, default=1)
    created_at              = Column(DateTime, nullable=False, server_default=func.now())
