# app/models/notification.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    related_url = Column(String, nullable=True)


    # New field for associating notifications with users
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="notifications")

