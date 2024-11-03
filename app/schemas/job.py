# # app/schemas/job.py
# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional

# class JobBase(BaseModel):
#     title: str
#     status: Optional[str] = "pending"

# class JobCreate(JobBase):
#     pass

# class Job(JobBase):
#     id: int
#     user_id: int
#     created_at: datetime
#     updated_at: Optional[datetime] = None

#     class Config:
#         from_attributes = True  # New way to enable ORM mode in Pydantic v2


# app/schemas/job.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict

class JobBase(BaseModel):
    title: str
    status: Optional[str] = "pending"
    active_days: Dict[str, bool] = Field(
        ...,
        description="Dictionary indicating if the job is active on each day",
        example={"MON": True, "TUE": False, "WED": True, "THU": False, "FRI": True, "SAT": False, "SUN": False}
    )
    at_from: str
    to: str
    every: Optional[str] = None

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Enabling ORM mode in Pydantic v2
