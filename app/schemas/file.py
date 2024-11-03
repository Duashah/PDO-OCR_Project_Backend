# # app/schemas/file.py
# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional, List

# class FileBase(BaseModel):
#     filename: str
#     status: str

# class FileCreate(FileBase):
#     pass

# class FileUpdate(BaseModel):
#     filename: Optional[str] = None
#     status: Optional[str] = None
#     auto_confirm: Optional[bool] = None

# class File(FileBase):
#     id: int
#     auto_confirm: bool
#     created_at: datetime
#     updated_at: Optional[datetime] = None  # Allow None for `updated_at`
#     user_id: int

#     class Config:
#         from_attributes = True  # New way to enable ORM mode in Pydantic v2

# class FileHistory(BaseModel):
#     id: int
#     action: str
#     details: Optional[str]
#     timestamp: datetime

#     class Config:
#         from_attributes = True  # New way to enable ORM mode in Pydantic v2





# app/schemas/file.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FileBase(BaseModel):
    file_id: str
    filename: str
    bl_number: str
    ship_to: Optional[str] = None
    carrier: Optional[str] = None
    stamp_type: Optional[str] = None
    pod_date: Optional[datetime] = None
    signature: Optional[str] = None
    issued_qty: Optional[int] = None
    received_qty: Optional[int] = None
    none_qty: Optional[int] = None
    dama_qty: Optional[int] = None
    short_qty: Optional[int] = None
    overa_qty: Optional[int] = None
    refus_qty: Optional[int] = None
    seal_i: Optional[str] = None
    recognition_status: str
    review_status: str
    reviewed_by: Optional[str] = None
    created_on: datetime
    changed_on: Optional[datetime] = None

class FileCreate(FileBase):
    pass

class FileUpdate(BaseModel):
    file_id: Optional[str] = None
    filename: Optional[str] = None
    bl_number: Optional[str] = None
    ship_to: Optional[str] = None
    carrier: Optional[str] = None
    stamp_type: Optional[str] = None
    pod_date: Optional[datetime] = None
    signature: Optional[str] = None
    issued_qty: Optional[int] = None
    received_qty: Optional[int] = None
    none_qty: Optional[int] = None
    dama_qty: Optional[int] = None
    short_qty: Optional[int] = None
    overa_qty: Optional[int] = None
    refus_qty: Optional[int] = None
    seal_i: Optional[str] = None
    recognition_status: Optional[str] = None
    review_status: Optional[str] = None
    reviewed_by: Optional[str] = None
    changed_on: Optional[datetime] = None

class File(FileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # Enable ORM mode in Pydantic v2


class FileHistory(BaseModel):
    id: int
    action: str
    details: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True  # New way to enable ORM mode in Pydantic v2
