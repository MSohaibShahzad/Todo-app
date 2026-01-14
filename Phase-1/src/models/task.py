"""Task model for the Todo application."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a single todo item with intermediate/advanced features.

    Phase-1 Attributes (Required):
        id: Unique sequential identifier
        title: Task summary (required, max 200 chars)
        description: Detailed task information (optional, max 1000 chars)
        is_complete: Completion status (False = incomplete, True = complete)

    Phase-2 Attributes (Optional):
        priority: Task priority level (Optional[str], "low"|"medium"|"high"|None)
        category: Task category/project (Optional[str], max 50 chars)
        due_date: Task deadline (Optional[datetime], must be future)
        recurrence_rule: Recurrence pattern (Optional[str], "daily"|"weekly"|"monthly"|None)
    """
    # Phase-1 fields
    id: int
    title: str
    description: str = ""
    is_complete: bool = False

    # Phase-2 fields
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence_rule: Optional[str] = None
