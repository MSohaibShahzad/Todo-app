# Data Model: Conversational AI

**Feature**: 004-conversational-ai
**Date**: 2026-01-15
**Status**: Complete

## Overview

This document defines the data models required for conversational AI functionality. All models persist in the existing PostgreSQL database (Neon) and follow SQLModel patterns established in Phase 2.

## Entity Relationship Diagram

```
User (existing)
  ↓ 1:N
Conversation
  ↓ 1:N
Message
  ↓ 0:N
ToolExecution
```

## Entities

### 1. Conversation

Represents a chat session between a user and the AI assistant.

**Purpose**: Groups related messages together, enables conversation management, supports concurrent conversations per user.

**Lifecycle**:
- Created when user starts new conversation
- Updated with each new message
- Automatically deleted after 30 days of inactivity
- Archived when user explicitly closes conversation

**SQLModel Definition**:

```python
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Conversation(SQLModel, table=True):
    """Conversation model for chat sessions."""

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, max_length=255, foreign_key="users.id")
    title: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation", cascade_delete=True)
```

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `id` | int | Auto | Primary key | Unique, auto-increment |
| `user_id` | str | Yes | Foreign key to users table | Must exist in users table |
| `title` | str | No | Optional conversation title (e.g., "Work tasks discussion") | Max 255 chars |
| `is_active` | bool | Yes | Whether conversation is currently active | Default: true |
| `created_at` | datetime | Auto | When conversation was created | UTC timestamp |
| `updated_at` | datetime | Auto | Last message timestamp | UTC timestamp, indexed for retention policy |

**Indexes**:
- `idx_conversations_user_id` on `user_id` (for listing user conversations)
- `idx_conversations_updated_at` on `updated_at` (for retention policy cleanup)
- `idx_conversations_is_active` on `is_active` (for active conversation queries)

**Constraints**:
- User can have max 3 active conversations (`is_active = true`)
- Conversations older than 30 days (by `updated_at`) are auto-deleted
- Deleting conversation cascades to all messages and tool executions

### 2. Message

Represents a single message in a conversation (from user or assistant).

**Purpose**: Stores conversation history for context, enables conversation replay, tracks tool usage per message.

**Lifecycle**:
- Created when user sends message or assistant responds
- Immutable once created (no updates)
- Deleted when parent conversation is deleted (cascade)

**SQLModel Definition**:

```python
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship, JSON, Column


class MessageRole(str, Enum):
    """Message sender role."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(SQLModel, table=True):
    """Message model for conversation messages."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(index=True, foreign_key="conversations.id")
    role: MessageRole = Field(max_length=50)
    content: str = Field()
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
    tool_executions: list["ToolExecution"] = Relationship(back_populates="message", cascade_delete=True)
```

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `id` | int | Auto | Primary key | Unique, auto-increment |
| `conversation_id` | int | Yes | Foreign key to conversations | Must exist in conversations |
| `role` | MessageRole | Yes | Sender role (user/assistant/system) | Enum: user, assistant, system |
| `content` | str | Yes | Message text content | Min 1 char, max 10,000 chars |
| `tool_calls` | dict | No | JSON structure of tool calls made by assistant | Stored as JSONB |
| `created_at` | datetime | Auto | When message was created | UTC timestamp |

**Indexes**:
- `idx_messages_conversation_id` on `conversation_id` (for retrieving conversation history)
- `idx_messages_created_at` on `created_at` (for chronological ordering)

**Constraints**:
- Messages are immutable (no updates after creation)
- `content` cannot be empty string
- `tool_calls` only populated for assistant messages that called tools

**tool_calls JSON Structure**:

```json
{
  "calls": [
    {
      "tool_name": "add_task",
      "parameters": {
        "title": "Buy groceries",
        "priority": "high",
        "due_date": "2026-01-16"
      },
      "result": "Task created: ID 42"
    }
  ]
}
```

### 3. ToolExecution

Represents a single tool invocation by the AI agent during a conversation.

**Purpose**: Audit trail of all tool calls, enables undo functionality, tracks success/failure rates.

**Lifecycle**:
- Created when agent calls a tool (before execution)
- Updated with result after tool execution completes
- Deleted when parent message is deleted (cascade)

**SQLModel Definition**:

```python
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship, JSON, Column


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
    status: ToolExecutionStatus = Field(default=ToolExecutionStatus.PENDING)
    error_message: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    # Relationships
    message: Optional["Message"] = Relationship(back_populates="tool_executions")
```

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `id` | int | Auto | Primary key | Unique, auto-increment |
| `message_id` | int | Yes | Foreign key to messages | Must exist in messages |
| `conversation_id` | int | Yes | Foreign key to conversations (denormalized for queries) | Must exist in conversations |
| `tool_name` | str | Yes | Name of MCP tool called | Max 100 chars |
| `parameters` | dict | Yes | Input parameters passed to tool | Stored as JSONB |
| `result` | dict | No | Tool execution result | Stored as JSONB |
| `status` | ToolExecutionStatus | Yes | Execution status | Enum: pending, success, failed |
| `error_message` | str | No | Error details if failed | Max 1000 chars |
| `created_at` | datetime | Auto | When tool call started | UTC timestamp |
| `completed_at` | datetime | No | When tool execution finished | UTC timestamp |

**Indexes**:
- `idx_tool_executions_message_id` on `message_id`
- `idx_tool_executions_conversation_id` on `conversation_id` (for undo last action)
- `idx_tool_executions_status` on `status` (for monitoring success rates)

**Constraints**:
- `result` populated only when `status = SUCCESS`
- `error_message` populated only when `status = FAILED`
- `completed_at` must be >= `created_at`

## State Transitions

### Conversation States

```
[Created] → is_active=true
    ↓
[Active] → receiving messages
    ↓
[Archived] → is_active=false (user closes)
    ↓
[Deleted] → auto-deleted after 30 days
```

**State Rules**:
- User can have max 3 conversations in `[Active]` state
- Starting 4th conversation auto-archives oldest inactive conversation
- `updated_at` refreshed on every new message
- Conversations in `[Archived]` state are read-only

### Tool Execution States

```
[Created] → status=PENDING
    ↓
[Executing] → tool function called
    ↓
[Completed] → status=SUCCESS (result populated)
    OR
[Failed] → status=FAILED (error_message populated)
```

**State Rules**:
- Status cannot transition back to PENDING after SUCCESS/FAILED
- `completed_at` timestamp required for SUCCESS/FAILED
- Failures logged but don't block conversation flow

## Validation Rules

### Conversation Validation

```python
from datetime import datetime, timedelta
from sqlalchemy import select, func

async def validate_active_conversation_limit(user_id: str, session: AsyncSession) -> bool:
    """Ensure user has fewer than 3 active conversations."""
    stmt = select(func.count()).where(
        Conversation.user_id == user_id,
        Conversation.is_active == True
    )
    count = await session.scalar(stmt)
    return count < 3


async def auto_delete_old_conversations(session: AsyncSession) -> int:
    """Delete conversations older than 30 days. Returns count deleted."""
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    stmt = select(Conversation).where(Conversation.updated_at < cutoff_date)
    old_conversations = await session.scalars(stmt)
    deleted_count = 0
    for conv in old_conversations:
        await session.delete(conv)
        deleted_count += 1
    await session.commit()
    return deleted_count
```

### Message Validation

```python
def validate_message_content(content: str) -> bool:
    """Validate message content."""
    if not content or not content.strip():
        raise ValueError("Message content cannot be empty")
    if len(content) > 10000:
        raise ValueError("Message content exceeds 10,000 character limit")
    return True


def validate_tool_calls_structure(tool_calls: dict) -> bool:
    """Validate tool_calls JSON structure."""
    if not isinstance(tool_calls, dict):
        return False
    if "calls" not in tool_calls:
        return False
    if not isinstance(tool_calls["calls"], list):
        return False
    for call in tool_calls["calls"]:
        if not all(k in call for k in ["tool_name", "parameters"]):
            return False
    return True
```

## Database Migration

### Migration Script (Alembic)

**File**: `backend/alembic/versions/002_add_conversations.py`

```python
"""Add conversations and messages tables

Revision ID: 002
Revises: 001
Create Date: 2026-01-15

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_updated_at', 'conversations', ['updated_at'])
    op.create_index('idx_conversations_is_active', 'conversations', ['is_active'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])

    # Create tool_executions table
    op.create_table(
        'tool_executions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('tool_name', sa.String(length=100), nullable=False),
        sa.Column('parameters', JSONB, nullable=False),
        sa.Column('result', JSONB, nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('error_message', sa.String(length=1000), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_tool_executions_message_id', 'tool_executions', ['message_id'])
    op.create_index('idx_tool_executions_conversation_id', 'tool_executions', ['conversation_id'])
    op.create_index('idx_tool_executions_status', 'tool_executions', ['status'])


def downgrade() -> None:
    op.drop_table('tool_executions')
    op.drop_table('messages')
    op.drop_table('conversations')
```

## Query Patterns

### Common Queries

**Get user's active conversations**:
```python
async def get_active_conversations(user_id: str, session: AsyncSession) -> list[Conversation]:
    stmt = select(Conversation).where(
        Conversation.user_id == user_id,
        Conversation.is_active == True
    ).order_by(Conversation.updated_at.desc())
    result = await session.scalars(stmt)
    return list(result)
```

**Load conversation history**:
```python
async def get_conversation_messages(
    conversation_id: int,
    user_id: str,
    limit: int = 20,
    session: AsyncSession
) -> list[Message]:
    """Get last N messages for conversation context."""
    # Verify ownership
    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    conversation = await session.scalar(stmt)
    if not conversation:
        raise ValueError("Conversation not found or access denied")

    # Get messages
    stmt = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.desc()).limit(limit)
    result = await session.scalars(stmt)
    messages = list(result)
    return list(reversed(messages))  # Return chronological order
```

**Get last tool execution for undo**:
```python
async def get_last_tool_execution(
    conversation_id: int,
    session: AsyncSession
) -> Optional[ToolExecution]:
    """Get most recent successful tool execution for undo functionality."""
    stmt = select(ToolExecution).where(
        ToolExecution.conversation_id == conversation_id,
        ToolExecution.status == ToolExecutionStatus.SUCCESS
    ).order_by(ToolExecution.completed_at.desc()).limit(1)
    return await session.scalar(stmt)
```

## Performance Estimates

### Storage Requirements

**Per User (30 days)**:
- Active conversations: ~3 × 500 bytes = 1.5 KB
- Messages: ~100 messages × 500 bytes = 50 KB
- Tool executions: ~50 executions × 1 KB = 50 KB
- **Total**: ~100 KB per user per month

**System (1000 users)**:
- Total storage: ~100 MB per month
- Growth rate: ~100 MB/month
- Database size after 1 year: ~1.2 GB (with 30-day retention)

### Query Performance

**Conversation retrieval** (with indexes):
- Expected: < 50ms for 20 messages
- Max: < 100ms with 1000 messages

**Tool execution lookup**:
- Expected: < 10ms (indexed by conversation_id)

**Retention cleanup** (scheduled daily):
- Batch delete: ~1000 conversations/minute
- Cascading deletes: messages and tool_executions cleaned automatically

## Data Retention Policy

### Automatic Cleanup (Scheduled Job)

**Schedule**: Daily at 2:00 AM UTC

**Process**:
1. Identify conversations with `updated_at` < 30 days ago
2. Batch delete in chunks of 100
3. Log deletion count and duration
4. Alert if cleanup takes > 5 minutes

**Implementation**:
```python
# backend/src/services/cleanup_service.py
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

async def cleanup_old_conversations(session: AsyncSession) -> dict:
    """Delete conversations older than 30 days."""
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    deleted_count = await auto_delete_old_conversations(session)
    return {
        "deleted_count": deleted_count,
        "cutoff_date": cutoff_date.isoformat()
    }
```

## Relationships with Existing Models

### User → Conversation (1:N)

- Each user can have multiple conversations
- Conversations deleted when user deleted (cascade)
- Active conversation limit: 3 per user

### Task (Existing) → No Direct Relationship

- Tasks accessed by AI agents via MCP tools
- Tool executions reference tasks indirectly (via tool parameters/results)
- No foreign key constraint between tasks and tool_executions (loose coupling)

## Summary

This data model supports:
- ✅ Stateless backend (state in database, not memory)
- ✅ Conversation history persistence
- ✅ Tool execution audit trail
- ✅ 30-day retention policy
- ✅ Concurrent conversation limit (3 per user)
- ✅ Undo functionality (last tool execution tracking)
- ✅ Scalable query patterns with proper indexes
- ✅ Cascading deletes for data cleanup

All models follow established SQLModel patterns from Phase 2 and integrate cleanly with existing authentication (user_id from Better-Auth).
