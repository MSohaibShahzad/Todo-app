"""Task Pydantic schemas for API."""
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, computed_field

from src.models.task import Priority, Recurrence


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    category: Optional[str] = Field(None, max_length=100)
    due_date: Optional[datetime] = None
    recurrence: Recurrence = Recurrence.NONE


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[Priority] = None
    category: Optional[str] = Field(None, max_length=100)
    due_date: Optional[datetime] = None
    recurrence: Optional[Recurrence] = None


class TaskResponse(BaseModel):
    """T100: Schema for task API responses with computed overdue/due_today fields."""

    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: Priority
    category: Optional[str]
    due_date: Optional[datetime]
    recurrence: Recurrence
    created_at: datetime
    updated_at: datetime

    @computed_field  # type: ignore[misc]
    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if not self.due_date or self.completed:
            return False
        now = datetime.now(timezone.utc)
        # Make due_date timezone-aware if it isn't
        due = self.due_date
        if due.tzinfo is None:
            due = due.replace(tzinfo=timezone.utc)
        return due < now

    @computed_field  # type: ignore[misc]
    @property
    def is_due_today(self) -> bool:
        """Check if task is due today."""
        if not self.due_date or self.completed:
            return False
        now = datetime.now(timezone.utc)
        # Make due_date timezone-aware if it isn't
        due = self.due_date
        if due.tzinfo is None:
            due = due.replace(tzinfo=timezone.utc)
        return due.date() == now.date()

    class Config:
        """Pydantic config."""

        from_attributes = True
