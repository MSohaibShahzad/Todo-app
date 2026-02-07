"""Tool execution database model."""
from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Column, Field, Relationship, SQLModel, JSON

if TYPE_CHECKING:
    from .message import Message


class ToolExecutionStatus(str, Enum):
    """Tool execution status."""

    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class ToolExecution(SQLModel, table=True):
    """Tool execution model for tracking tool calls."""

    __tablename__ = "tool_executions"

    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: int = Field(index=True, foreign_key="messages.id")
    conversation_id: int = Field(index=True, foreign_key="conversations.id")
    tool_name: str = Field(max_length=100)
    parameters: dict = Field(sa_column=Column(JSON))
    result: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    status: ToolExecutionStatus = Field(default=ToolExecutionStatus.PENDING, index=True)
    error_message: Optional[str] = Field(default=None, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    # Relationships
    message: Optional["Message"] = Relationship(back_populates="tool_executions")
