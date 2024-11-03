# app/api/database_connection.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.database_connection import DatabaseConnectionSchema
from app.models.database_connection import DatabaseConnection
from app.core.database import get_db

router = APIRouter()

@router.post("/db-connection", status_code=status.HTTP_201_CREATED)
async def create_db_connection(
    db_conn: DatabaseConnectionSchema, db: AsyncSession = Depends(get_db)
):
    # Check if system ID already exists
    stmt = select(DatabaseConnection).where(DatabaseConnection.system_id == db_conn.system_id)
    result = await db.execute(stmt)
    existing_connection = result.scalars().first()

    if existing_connection:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="System ID already exists."
        )
    
    # Save the new database connection
    new_db_conn = DatabaseConnection(
        system_id=db_conn.system_id,
        username=db_conn.username,
        password=db_conn.password,  # Consider hashing the password
        ip_address=db_conn.ip_address,
        port=db_conn.port,
        service_name=db_conn.service_name
    )
    db.add(new_db_conn)
    await db.commit()
    await db.refresh(new_db_conn)

    return {"message": "Database connection created successfully", "connection_id": new_db_conn.id}
