"""Application configuration settings."""
import os
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/todoapp"

    # JWT Configuration
    jwt_secret: str = "your-secret-key-change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    # CORS
    frontend_url: str = "http://localhost:3000"

    # Environment
    environment: Literal["development", "production", "test"] = "development"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
