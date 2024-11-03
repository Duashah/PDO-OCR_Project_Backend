# # app/models/file.py
# from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from app.core.database import Base

# class File(Base):
#     __tablename__ = "files"
    
#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String)
#     status = Column(String)
#     auto_confirm = Column(Boolean, default=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#     user_id = Column(Integer, ForeignKey("users.id"))
    
#     # Add relationship back to User
#     user = relationship("User", back_populates="files")
#     history = relationship("FileHistory", back_populates="file", cascade="all, delete-orphan")
# app/models/file.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, unique=True, nullable=False)          # File ID
    filename = Column(String, nullable=False)                       # File Name
    bl_number = Column(String, nullable=False)                      # B/L Number
    ship_to = Column(String, nullable=True)                         # Ship-to
    carrier = Column(String, nullable=True)                         # Carrier
    stamp_type = Column(String, nullable=True)                      # Stamp Type
    pod_date = Column(DateTime, nullable=True)                      # POD Date
    signature = Column(String, nullable=True)                       # Signature
    issued_qty = Column(Integer, nullable=True)                     # Issued Qty
    received_qty = Column(Integer, nullable=True)                   # Received Qty
    none_qty = Column(Integer, nullable=True)                       # None Qty
    dama_qty = Column(Integer, nullable=True)                       # Dama Qty
    short_qty = Column(Integer, nullable=True)                      # Short Qty
    overa_qty = Column(Integer, nullable=True)                      # Overa Qty
    refus_qty = Column(Integer, nullable=True)                      # Refus Qty
    seal_i = Column(String, nullable=True)                          # Seal I
    recognition_status = Column(String, nullable=False)             # Recognition Status
    review_status = Column(String, nullable=False)                  # Review Status
    reviewed_by = Column(String, nullable=True)                     # Reviewed By
    created_on = Column(DateTime, nullable=False, server_default=func.now())  # Created On
    changed_on = Column(DateTime, nullable=True, onupdate=func.now())         # Changed On

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="files")
    history = relationship("FileHistory", back_populates="file", cascade="all, delete-orphan")


class FileHistory(Base):
    __tablename__ = "file_history"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    action = Column(String)
    details = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    file = relationship("File", back_populates="history")