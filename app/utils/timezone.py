# app/utils/timezone.py
from datetime import datetime
import pytz

def convert_to_user_timezone(dt: datetime, timezone: str) -> datetime:
    utc_dt = dt.astimezone(pytz.utc) if dt.tzinfo is None else dt
    user_timezone = pytz.timezone(timezone)
    return utc_dt.astimezone(user_timezone)
