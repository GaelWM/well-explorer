import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict# type: ignore
from pydantic import field_validator # type: ignore


class Settings(BaseSettings):
    model_config = SettingsConfigDict(enable_decoding=False, case_sensitive=True)

    # General
    PROJECT_NAME: str = "Well Explorer Backend API"
    PROJECT_DESCRIPTION: str = "A FastAPI backend for the Well Explorer application"
    PROJECT_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    CORS_ORIGINS: List[str] = ['http://localhost:4200', 'http://localhost:4300', 'http://localhost:8000']

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def split_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/app_db"
    )

settings = Settings()