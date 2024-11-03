# # app/api/jobs.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from typing import List
# from app.core.database import get_db
# from app.models.job import Job
# from app.schemas.job import JobCreate, Job as JobSchema
# from app.utils.auth import get_current_user

# router = APIRouter()
# @router.post("/jobs/", response_model=JobSchema)
# async def create_job(
#     job: JobCreate,
#     db: AsyncSession = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     db_job = Job(
#         title=job.title,
#         status=job.status,
#         user_id=current_user.id
#     )
#     db.add(db_job)
#     await db.commit()
#     await db.refresh(db_job)
#     return db_job

# @router.get("/jobs/", response_model=List[JobSchema])
# async def get_jobs_by_status(
#     status: str,
#     db: AsyncSession = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     query = select(Job).where(
#         Job.status == status,
#         Job.user_id == current_user.id
#     )
#     result = await db.execute(query)
#     jobs = result.scalars().all()
#     return jobs or []

# @router.delete("/jobs/{job_id}")
# async def delete_job(
#     job_id: int,
#     db: AsyncSession = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     query = select(Job).where(
#         Job.id == job_id,
#         Job.user_id == current_user.id
#     )
    
#     result = await db.execute(query)
#     job = result.scalar_one_or_none()

#     if not job:
#         raise HTTPException(status_code=404, detail="Job not found")
    
#     await db.delete(job)
#     await db.commit()
#     return {"message": "Job deleted successfully"}



# app/api/jobs.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, Job as JobSchema
from app.utils.auth import get_current_user
from typing import Optional

router = APIRouter()

@router.post("/jobs/", response_model=JobSchema)
async def create_job(
    job: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_job = Job(
        title=job.title,
        status=job.status,
        active_days=job.active_days,
        at_from=job.at_from,
        to=job.to,
        every=job.every,
        user_id=current_user.id
    )
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job

@router.get("/jobs/", response_model=List[JobSchema])
async def get_jobs(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = select(Job).where(Job.user_id == current_user.id)
    
    # Apply status filter only if a status is provided
    if status:
        query = query.where(Job.status == status)
        
    result = await db.execute(query)
    jobs = result.scalars().all()
    return jobs or []

@router.get("/jobs/search/", response_model=List[JobSchema])
async def search_job(
    title: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Search for jobs with the title that belongs to the current user
    query = select(Job).where(
        Job.title.ilike(f"%{title}%"),  # Case-insensitive search for partial matches
        Job.user_id == current_user.id
    )
    result = await db.execute(query)
    jobs = result.scalars().all()
    return jobs or []

@router.delete("/jobs/{job_id}")
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = select(Job).where(
        Job.id == job_id,
        Job.user_id == current_user.id
    )
    
    result = await db.execute(query)
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    await db.delete(job)
    await db.commit()
    return {"message": "Job deleted successfully"}
