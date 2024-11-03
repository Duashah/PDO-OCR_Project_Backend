# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import timedelta
from typing import Any
from app.core.database import get_db, settings
from app.models.user import User
from app.schemas.user import UserCreate, Token, User as UserSchema
from app.utils.timezone import convert_to_user_timezone
from app.utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)

# app/api/auth.py (add these new endpoints)
from datetime import datetime, timedelta
from app.utils.email import generate_otp, send_email
# from app.templates.email_templates import get_reset_password_template
from app.schemas.auth import PasswordResetRequest, VerifyOTP, PasswordReset

from app.utils.auth import create_password_reset_token, verify_password_reset_token
from app.templates.email_templates import get_reset_password_link_template

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup-login", response_model=Token)
async def signup_login(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> Any:
    # Check if email or phone number is already registered
    query = select(User).where((User.email == user_data.email) | (User.phone_number == user_data.phone_number))
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone number already registered"
        )

    # Check if password and confirm_password match
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Create new user
    db_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone_number=user_data.phone_number
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # Login the user immediately after signup
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}












@router.post("/signup", response_model=UserSchema)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> Any:
    # Check if email or phone number is already registered
    query = select(User).where((User.email == user_data.email) | (User.phone_number == user_data.phone_number))
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone number already registered"
        )
    
    # Check if password and confirm_password match
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Create new user
    db_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone_number=user_data.phone_number
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Any:
    # Authenticate user
    query = select(User).where(User.email == form_data.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/me", response_model=UserSchema)
# async def read_users_me(current_user: User = Depends(get_current_user)) -> Any:
#     return current_user



@router.post("/forgot-password")
async def forgot_password(
    request_data: PasswordResetRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Any:
    # Find user
    query = select(User).where(User.email == request_data.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        # Return success even if user doesn't exist (security)
        return {"message": "If the email exists, a password reset OTP has been sent."}
    
    # # Generate and save OTP
    # otp = generate_otp()
    # user.otp = get_password_hash(otp)  # Hash OTP for security
    # user.otp_created_at = datetime.utcnow()
    
    # Generate password reset token
    token = create_password_reset_token({"sub": user.email})
    reset_link = f"{request.url_for('reset_password')}?token={token}"

    # try:
    #     await db.commit()
        
    #     # Send email
    #     email_template = get_reset_password_template(otp)
    #     email_sent = await send_email(
    #         to_email=user.email,
    #         subject="Password Reset Request",
    #         body=email_template
    #     )
        
    #     if not email_sent:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail="Failed to send email"
    #         )
        
    #     return {"message": "If the email exists, a password reset OTP has been sent."}
    # except Exception as e:
    #     await db.rollback()
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=str(e)
    #     )

    try:
        # Send email with reset link
        email_template = get_reset_password_link_template(reset_link)
        email_sent = await send_email(
            to_email=user.email,
            subject="Password Reset Request",
            body=email_template
        )
        
        if not email_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email"
            )
        
        return {"message": "If the email exists, a password reset link has been sent."}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/verify-otp")
async def verify_otp(
    verify_data: VerifyOTP,
    db: AsyncSession = Depends(get_db)
) -> Any:
    # Find user
    query = select(User).where(User.email == verify_data.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user or not user.otp or not user.otp_created_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Check OTP expiry
    expiry_time = user.otp_created_at + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
    if datetime.utcnow() > expiry_time:
        # Clear expired OTP
        user.otp = None
        user.otp_created_at = None
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired"
        )
    
    # Verify OTP
    if not verify_password(verify_data.otp, user.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    
    return {"message": "OTP verified successfully"}

# @router.post("/reset-password")
# async def reset_password(
#     reset_data: PasswordReset,
#     db: AsyncSession = Depends(get_db)
# ) -> Any:
#     # Find user
#     query = select(User).where(User.email == reset_data.email)
#     result = await db.execute(query)
#     user = result.scalar_one_or_none()
    
#     if not user or not user.otp or not user.otp_created_at:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid or expired reset request"
#         )
    
#     # Verify OTP again
#     if not verify_password(reset_data.otp, user.otp):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid OTP"
#         )
    
#     # Update password
#     user.hashed_password = get_password_hash(reset_data.new_password)
#     user.otp = None
#     user.otp_created_at = None
    
#     try:
#         await db.commit()
#         return {"message": "Password reset successful"}
#     except Exception as e:
#         await db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e)
#         )


@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordReset,
    db: AsyncSession = Depends(get_db),
    token: str = ""
) -> Any:
    # Verify token
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    # Find user
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset request"
        )

    # Update password
    user.hashed_password = get_password_hash(reset_data.new_password)
    
    try:
        await db.commit()
        return {"message": "Password reset successful"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    



@router.put("/user/timezone", response_model=UserSchema)
async def set_timezone(
    timezone: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Update timezone for the current user
    query = update(User).where(User.id == current_user.id).values(timezone=timezone)
    await db.execute(query)
    await db.commit()
    # Return updated user information
    user = await db.get(User, current_user.id)
    return user