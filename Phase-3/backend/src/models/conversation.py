"""Conversation database model."""
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .message import Message


class Conversation(SQLModel, table=True):
    """Conversation model for chat sessions."""

    __tablename__ = "conversations"

    id: str = Field(primary_key=True, max_length=255)
    user_id: str = Field(index=True, max_length=255, foreign_key="users.id")
    title: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation", cascade_delete=True)
