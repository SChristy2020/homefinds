from datetime import datetime, timezone, timedelta
from typing import Annotated
from pydantic import PlainSerializer

_EASTERN = timezone(timedelta(hours=-4))

def _eastern_naive_to_utc_str(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_EASTERN)
    return dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')

def _utc_naive_to_utc_str(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')

UTCNaiveDatetime = Annotated[datetime, PlainSerializer(_utc_naive_to_utc_str, return_type=str, when_used='always')]
EasternNaiveDatetime = Annotated[datetime, PlainSerializer(_eastern_naive_to_utc_str, return_type=str, when_used='always')]
