# app/schemas/notification.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationBase(BaseModel):
    text: str
    related_url: Optional[str] = None

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True  # Enable ORM mode
