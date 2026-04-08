import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'pickup_settings.json')

DEFAULTS = {
    "endDate": "2026-04-25",
    "defaultDate": "2026-04-18",
    "startHour": 10,
    "endHour": 20,
    "defaultHour": 15,
    "defaultMinute": "00",
    "minuteInterval": 15,
    "minutes": ["00", "15", "30", "45"],
    "blockedRanges": [],
}


def _read() -> dict:
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {**DEFAULTS, **data}
    except FileNotFoundError:
        return dict(DEFAULTS)


def _write(data: dict):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class BlockedRange(BaseModel):
    date: str
    startHour: int
    endHour: int


class PickupSettingsIn(BaseModel):
    endDate: str
    defaultDate: str
    startHour: int
    endHour: int
    defaultHour: int
    defaultMinute: str
    minuteInterval: int
    minutes: List[str]
    blockedRanges: List[BlockedRange] = []


@router.get("")
def get_pickup_settings():
    return _read()


@router.put("")
def save_pickup_settings(body: PickupSettingsIn):
    data = body.model_dump()
    _write(data)
    return data
