"""T097-T098: Recurrence service for calculating next due dates and creating recurring instances."""
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Recurrence, Task


def calculate_next_due_date(current_due: datetime, recurrence: Recurrence) -> datetime:
    """T097: Calculate the next due date based on recurrence pattern.

    Args:
        current_due: Current due date
        recurrence: Recurrence pattern (none, daily, weekly, monthly)

    Returns:
        Next due date based on recurrence pattern
    """
    if recurrence == Recurrence.NONE:
        return current_due

    if recurrence == Recurrence.DAILY:
        return current_due + timedelta(days=1)

    if recurrence == Recurrence.WEEKLY:
        return current_due + timedelta(weeks=1)

    if recurrence == Recurrence.MONTHLY:
        # Add approximately one month (30 days for simplicity)
        # For production, use dateutil.relativedelta for accurate month handling
        next_month = current_due + timedelta(days=30)
        # Try to keep the same day of month
        try:
            return next_month.replace(day=current_due.day)
        except ValueError:
            # If day doesn't exist in next month (e.g., Jan 31 -> Feb 31), use last day
            return next_month

    return current_due


async def create_recurring_instance(
    db: AsyncSession, original_task: Task
) -> Optional[Task]:
    """T098: Create a new instance of a recurring task.

    Args:
        db: Database session
        original_task: The completed recurring task to duplicate

    Returns:
        New task instance with updated due date, or None if not recurring
    """
    # Only create new instance if task has recurrence and due date
    if (
        original_task.recurrence == Recurrence.NONE
        or not original_task.due_date
    ):
        return None

    # Calculate next due date
    next_due = calculate_next_due_date(original_task.due_date, original_task.recurrence)

    # Create new task instance
    new_task = Task(
        user_id=original_task.user_id,
        title=original_task.title,
        description=original_task.description,
        priority=original_task.priority,
        category=original_task.category,
        due_date=next_due,
        recurrence=original_task.recurrence,
        completed=False,  # New instance starts as incomplete
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task
