


# app/utils/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.job import Job
from app.models.file import File
from app.core.database import get_db
from sqlalchemy import select
from datetime import datetime
import random

# Initialize the scheduler
scheduler = AsyncIOScheduler()

# Updated dummy OCR function
async def dummy_ocr_process(file: File, db: AsyncSession):
    # Populate file fields with dummy OCR data
    file.bl_number = f"BL{random.randint(1000, 9999)}"              # Random B/L Number
    file.ship_to = f"Location {random.randint(1, 50)}"              # Random Ship-to location
    file.carrier = f"Carrier {random.choice(['A', 'B', 'C'])}"      # Random Carrier
    file.stamp_type = random.choice(["Type1", "Type2", "Type3"])    # Random Stamp Type
    file.pod_date = datetime.utcnow()                               # Current date for POD Date
    file.signature = f"Sig {random.choice(['X', 'Y', 'Z'])}"        # Random Signature
    file.issued_qty = random.randint(1, 1000)                       # Random Issued Qty
    file.received_qty = random.randint(1, 1000)                     # Random Received Qty
    file.none_qty = random.randint(0, 10)                           # Random None Qty
    file.dama_qty = random.randint(0, 10)                           # Random Dama Qty
    file.short_qty = random.randint(0, 10)                          # Random Short Qty
    file.overa_qty = random.randint(0, 10)                          # Random Overa Qty
    file.refus_qty = random.randint(0, 10)                          # Random Refus Qty
    file.seal_i = f"Seal{random.randint(1, 5)}"                     # Random Seal I
    file.recognition_status = "Processed"                           # Set Recognition Status
    file.review_status = "Pending Review"                           # Set Review Status
    file.reviewed_by = "OCR System"                                 # OCR System as Reviewer
    file.changed_on = datetime.utcnow()                             # Update changed_on timestamp
    
    # Save dummy OCR data to the database
    db.add(file)  # Add to the session
    await db.commit()

# Task to run scheduled jobs
async def run_scheduled_jobs():
    async for db in get_db():  # Get the database session from the async generator
        async with db:
            # Fetch active jobs scheduled to run today
            current_day = datetime.utcnow().strftime("%a").upper()
            query = select(Job).where(Job.active_days.contains(current_day))
            result = await db.execute(query)
            jobs = result.scalars().all()

            for job in jobs:
                # Simulate fetching files for the current job
                query_files = select(File).where(File.user_id == job.user_id)
                files = (await db.execute(query_files)).scalars().all()

                for file in files:
                    await dummy_ocr_process(file, db)  # Process each file

            await db.commit()  # Commit the session after processing all files

# Start the scheduler with the job-running task
def start_scheduler():
    scheduler.add_job(run_scheduled_jobs, "interval", minutes=1)  # Runs every minute
    scheduler.start()
