# # app/models/job.py
# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from app.core.database import Base

# class Job(Base):
#     __tablename__ = "jobs"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     status = Column(String)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#     user_id = Column(Integer, ForeignKey("users.id"))
    
#     # Add relationship back to User
#     user = relationship("User", back_populates="jobs")


# app/models/job.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    
    # Using JSON field to store active days (MON to SUN)
    active_days = Column(JSON, nullable=False, default={
        "MON": False,
        "TUE": False,
        "WED": False,
        "THU": False,
        "FRI": False,
        "SAT": False,
        "SUN": False
    })
    
    # Additional job-related fields
    at_from = Column(String, nullable=False)  # Time the job starts or is scheduled
    to = Column(String, nullable=False)       # Time the job ends
    every = Column(String, nullable=True)     # Frequency, e.g., "Every 3 hours"
    status = Column(String, nullable=False)   # Active, Inactive, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign key and relationship
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="jobs")
