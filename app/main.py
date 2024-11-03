# app/main.py (update)
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from app.core.database import get_db, engine, Base
from app.api import auth, jobs, files, notifications, database_connection
from app.models.file import File
from app.utils.scheduler import start_scheduler
# In your FastAPI app, add CORS middleware
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="POD Delivery OCR Backend🔰",
    description="Backend API for POD Delivery OCR",
    version="0.1.0"
)

# Include routers
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(files.router)
app.include_router(notifications.router)
app.include_router(database_connection.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Start the scheduler
    start_scheduler()


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Project"}

@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    try:
        # Test the database connection using proper SQLAlchemy text construct
        result = await db.execute(text("SELECT 1"))
        await db.commit()
        return {
            "message": "Database connection successful!",
            "result": result.scalar()
        }
    except Exception as e:
        return {"error": f"Database connection failed: {str(e)}"}