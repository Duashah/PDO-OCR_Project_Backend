# app/api/notifications.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.notification import Notification as NotificationModel
from app.schemas.notification import Notification as NotificationSchema, NotificationCreate
from app.utils.auth import get_current_user
from app.utils.timezone import convert_to_user_timezone

router = APIRouter()

@router.get("/notifications/", response_model=List[NotificationSchema])
async def get_notifications(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = select(NotificationModel).where(NotificationModel.user_id == current_user.id)
    result = await db.execute(query)
    notifications = result.scalars().all()
    # Adjust timestamps according to user's timezone
    for notification in notifications:
        notification.timestamp = convert_to_user_timezone(notification.timestamp, current_user.timezone)
    return notifications or []
    

@router.post("/notifications/", response_model=NotificationSchema)
async def create_notification(
    notification_data: NotificationCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_notification = NotificationModel(
        text=notification_data.text,
        related_url=notification_data.related_url
    )
    db.add(new_notification)
    await db.commit()
    await db.refresh(new_notification)
    return new_notification
