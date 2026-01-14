"""Task service layer for business logic."""
from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate
from src.services import recurrence_service


async def create_task(
    db: AsyncSession, user_id: str, task_data: TaskCreate
) -> Task:
    """Create a new task for a user.

    Args:
        db: Database session
        user_id: ID of the user creating the task
        task_data: Task creation data

    Returns:
        Created task
    """
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        category=task_data.category,
        due_date=task_data.due_date,
        recurrence=task_data.recurrence,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_user_tasks(db: AsyncSession, user_id: str) -> Sequence[Task]:
    """Get all tasks for a user.

    Args:
        db: Database session
        user_id: ID of the user

    Returns:
        List of user's tasks
    """
    result = await db.execute(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    )
    return result.scalars().all()


async def get_task_by_id(
    db: AsyncSession, task_id: int, user_id: str
) -> Task | None:
    """Get a task by ID with ownership check.

    Args:
        db: Database session
        task_id: ID of the task
        user_id: ID of the user (for ownership verification)

    Returns:
        Task if found and owned by user, None otherwise
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def update_task(
    db: AsyncSession, task_id: int, user_id: str, task_data: TaskUpdate
) -> Task | None:
    """Update a task.

    Args:
        db: Database session
        task_id: ID of the task to update
        user_id: ID of the user (for ownership verification)
        task_data: Task update data

    Returns:
        Updated task if found and owned by user, None otherwise
    """
    task = await get_task_by_id(db, task_id, user_id)
    if not task:
        return None

    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: int, user_id: str) -> bool:
    """Delete a task.

    Args:
        db: Database session
        task_id: ID of the task to delete
        user_id: ID of the user (for ownership verification)

    Returns:
        True if task was deleted, False if not found or not owned by user
    """
    task = await get_task_by_id(db, task_id, user_id)
    if not task:
        return False

    await db.delete(task)
    await db.commit()
    return True


async def toggle_task_complete(
    db: AsyncSession, task_id: int, user_id: str, completed: bool
) -> Task | None:
    """T099: Toggle task completion status and create recurring instance if needed.

    Args:
        db: Database session
        task_id: ID of the task
        user_id: ID of the user (for ownership verification)
        completed: New completion status

    Returns:
        Updated task if found and owned by user, None otherwise
    """
    task = await get_task_by_id(db, task_id, user_id)
    if not task:
        return None

    task.completed = completed
    task.updated_at = datetime.utcnow()
    db.add(task)
    await db.commit()
    await db.refresh(task)

    # T099: Create recurring instance when marking recurring task as complete
    if completed and task.recurrence and task.due_date:
        await recurrence_service.create_recurring_instance(db, task)

    return task
