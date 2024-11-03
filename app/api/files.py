# app/api/files.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional
from app.core.database import get_db
from app.models.file import File as FileModel, FileHistory
from app.schemas.file import FileCreate, FileUpdate, File as FileSchema, FileHistory as FileHistorySchema
from app.utils.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/files/", response_model=List[FileSchema])
async def get_all_files(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = select(FileModel).where(FileModel.user_id == current_user.id)
    result = await db.execute(query)
    files = result.scalars().all()
    return files or []

@router.put("/files/{file_id}/auto-confirm")
async def enable_auto_confirm(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # First get the file
    query = select(FileModel).where(
        FileModel.id == file_id,
        FileModel.user_id == current_user.id
    )
    result = await db.execute(query)
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Update the file
    file.auto_confirm = True
    
    # Add history entry
    history = FileHistory(
        file_id=file.id,
        action="auto_confirm_enabled",
        details="Auto-confirm feature was enabled"
    )
    db.add(history)
    await db.commit()
    
    return {"message": "Auto-confirm enabled"}

# @router.put("/files/{file_id}", response_model=FileSchema)
# async def modify_file(
#     file_id: int,
#     file_data: FileUpdate,
#     db: AsyncSession = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     # First get the file
#     query = select(FileModel).where(
#         FileModel.id == file_id,
#         FileModel.user_id == current_user.id
#     )
#     result = await db.execute(query)
#     file = result.scalar_one_or_none()
    
#     if not file:
#         raise HTTPException(status_code=404, detail="File not found")
    
#     # Update only provided fields
#     update_data = file_data.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(file, key, value)
    
#     # Add history entry
#     history = FileHistory(
#         file_id=file.id,
#         action="modify",
#         details=f"File details updated: {', '.join(f'{k}={v}' for k, v in update_data.items())}"
#     )
#     db.add(history)
#     await db.commit()
#     await db.refresh(file)
    
#     return file



@router.put("/files/{file_id}", response_model=FileSchema)
async def modify_file(
    file_id: int,
    file_data: FileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Fetch the file and ensure it belongs to the current user
    query = select(FileModel).where(
        FileModel.id == file_id,
        FileModel.user_id == current_user.id
    )
    result = await db.execute(query)
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Update only fields provided in request
    update_data = file_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(file, key, value)
    
    # Add history entry for modifications
    history = FileHistory(
        file_id=file.id,
        action="modify",
        details=f"File details updated: {', '.join(f'{k}={v}' for k, v in update_data.items())}"
    )
    db.add(history)
    await db.commit()
    await db.refresh(file)
    
    return file

@router.delete("/files/{file_id}")
async def delete_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # First get the file
    query = select(FileModel).where(
        FileModel.id == file_id,
        FileModel.user_id == current_user.id
    )
    result = await db.execute(query)
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Add history entry before deletion
    history = FileHistory(
        file_id=file.id,
        action="delete",
        details="File was marked for deletion"
    )
    db.add(history)
    
    # Delete the file
    await db.delete(file)
    await db.commit()
    
    return {"message": "File deleted successfully"}

# @router.get("/files/search/", response_model=List[FileSchema])
# async def search_files(
#     query: str,
#     status: Optional[str] = None,
#     db: AsyncSession = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     filters = [
#         FileModel.filename.ilike(f"%{query}%"),
#         FileModel.user_id == current_user.id
#     ]
    
#     if status:
#         filters.append(FileModel.status == status)
    
#     stmt = select(FileModel).where(*filters)
#     result = await db.execute(stmt)
#     files = result.scalars().all()
#     return files or []



@router.get("/files/search/", response_model=List[FileSchema])
async def search_files(
    file_id: Optional[str] = None,
    bl_number: Optional[str] = None,
    filename: Optional[str] = None,
    recognition_status: Optional[str] = None,
    review_status: Optional[str] = None,
    changed_on: Optional[datetime] = None,
    ship_to: Optional[str] = None,
    carrier: Optional[str] = None,
    created_on: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Base query ensuring files are owned by the current user
    query = select(FileModel).where(FileModel.user_id == current_user.id)

    # Apply filters if parameters are provided
    if file_id:
        query = query.where(FileModel.file_id.ilike(f"%{file_id}%"))
    if bl_number:
        query = query.where(FileModel.bl_number.ilike(f"%{bl_number}%"))
    if filename:
        query = query.where(FileModel.filename.ilike(f"%{filename}%"))
    if recognition_status:
        query = query.where(FileModel.recognition_status == recognition_status)
    if review_status:
        query = query.where(FileModel.review_status == review_status)
    if changed_on:
        query = query.where(FileModel.changed_on == changed_on)
    if ship_to:
        query = query.where(FileModel.ship_to.ilike(f"%{ship_to}%"))
    if carrier:
        query = query.where(FileModel.carrier.ilike(f"%{carrier}%"))
    if created_on:
        query = query.where(FileModel.created_on == created_on)

    result = await db.execute(query)
    files = result.scalars().all()
    return files or []

@router.get("/history/{file_id}", response_model=List[FileHistorySchema])
async def get_file_history(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # First verify the file belongs to the user
    file_query = select(FileModel).where(
        FileModel.id == file_id,
        FileModel.user_id == current_user.id
    )
    file_result = await db.execute(file_query)
    file = file_result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get history
    history_query = select(FileHistory).where(
        FileHistory.file_id == file_id
    ).order_by(FileHistory.timestamp.desc())
    
    history_result = await db.execute(history_query)
    history = history_result.scalars().all()
    return history or []