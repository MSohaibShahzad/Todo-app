"""Message database model."""
from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Column, Field, Relationship, SQLModel, JSON

if TYPE_CHECKING:
    from .conversation import Conversation
    from .tool_execution import ToolExecution


class MessageRole(str, Enum):
    """Message sender role."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(SQLModel, table=True):
    """Message model for conversation messages."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(index=True, max_length=255, foreign_key="conversations.id")
    role: MessageRole = Field(max_length=50)
    content: str = Field()
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
    tool_executions: list["ToolExecution"] = Relationship(back_populates="message", cascade_delete=True)
