"""Conversation Pydantic schemas for API."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    """Schema for creating a new conversation."""

    title: Optional[str] = Field(None, max_length=255)
    initial_message: Optional[str] = Field(None, description="Optional first message to send")


class MessageCreate(BaseModel):
    """Schema for sending a message in a conversation."""

    content: str = Field(..., min_length=1, description="Message content from user")


class MessageResponse(BaseModel):
    """Schema for message response."""

    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class ToolExecutionResponse(BaseModel):
    """Schema for tool execution response."""

    id: int
    tool_name: str
    parameters: dict
    result: Optional[dict] = None
    status: str
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class SendMessageResponse(BaseModel):
    """Schema for send message endpoint response."""

    user_message: MessageResponse
    assistant_message: MessageResponse
    tool_executions: list[ToolExecutionResponse]


class ConversationResponse(BaseModel):
    """Schema for conversation response."""

    id: int
    user_id: str
    title: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    messages: Optional[list[MessageResponse]] = None

    class Config:
        """Pydantic config."""
        from_attributes = True
