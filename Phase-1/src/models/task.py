"""Task model for the Todo application."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique sequential identifier
        title: Task summary (required, max 200 chars)
        description: Detailed task information (optional, max 1000 chars)
        is_complete: Completion status (False = incomplete, True = complete)
    """
    id: int
    title: str
    description: str = ""
    is_complete: bool = False
