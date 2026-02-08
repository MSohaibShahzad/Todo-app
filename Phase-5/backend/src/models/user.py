"""User database model."""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User model for authentication."""

    __tablename__ = "users"

    id: str = Field(primary_key=True, max_length=255)  # Changed to string to match Better Auth
    email: Optional[str] = Field(default=None, unique=True, index=True, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    hashed_password: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
