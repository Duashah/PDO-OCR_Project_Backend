# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, constr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    # make phone number pattern to 11 digits 
    phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{10}$')  # E.164 format
    # phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')  # E.164 format
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)

    # Ensure password and confirm_password match
    @validator("confirm_password")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    timezone: Optional[str] = "UTC"  # Add timezone to user schema

    class Config:
        from_attributes = True




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