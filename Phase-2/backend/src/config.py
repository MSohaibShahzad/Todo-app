"""Application configuration settings."""
import os
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql+psycopg://user:password@localhost:5432/todoapp"

    @property
    def database_url_with_driver(self) -> str:
        """Ensure DATABASE_URL uses psycopg driver for SQLAlchemy."""
        url = self.database_url
        # Convert postgresql:// to postgresql+psycopg:// for psycopg3 driver
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        elif url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg://", 1)
        return url

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
