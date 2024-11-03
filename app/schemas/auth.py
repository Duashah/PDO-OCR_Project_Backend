from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PasswordResetRequest(BaseModel):
    email: EmailStr

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

# class PasswordReset(BaseModel):
#     email: EmailStr
#     otp: str
#     new_password: str

# app/schemas/auth.py
class PasswordReset(BaseModel):
    new_password: str