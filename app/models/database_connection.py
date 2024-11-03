# app/models/database_connection.py

from sqlalchemy import Column, Integer, String
from app.core.database import Base

class DatabaseConnection(Base):
    __tablename__ = "database_connections"

    id = Column(Integer, primary_key=True, index=True)
    system_id = Column(String, unique=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)  # You may want to hash this
    ip_address = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    service_name = Column(String, nullable=False)
