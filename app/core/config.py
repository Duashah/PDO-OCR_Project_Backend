# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db"
    
    # Security settings
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your-email@gmail.com"
    SMTP_PASSWORD: str = "your-app-password"
    OTP_EXPIRY_MINUTES: int = 15


    # File upload settings
    UPLOAD_DIR: str = "uploads/"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()