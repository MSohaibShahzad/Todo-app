"""Task API endpoints."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.database import get_session
from src.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from src.services import task_service

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: Annotated[str, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> TaskResponse:
    """Create a new task for the authenticated user.

    Args:
        task_data: Task creation data
        user_id: Authenticated user ID from JWT
        db: Database session

    Returns:
        Created task
    """
    task = await task_service.create_task(db, user_id, task_data)
    return TaskResponse.model_validate(task)


@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(
    user_id: Annotated[str, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> list[TaskResponse]:
    """Get all tasks for the authenticated user.

    Args:
        user_id: Authenticated user ID from JWT
        db: Database session

    Returns:
        List of user's tasks
    """
    tasks = await task_service.get_user_tasks(db, user_id)
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/tasks/summary")
async def get_tasks_summary(
    user_id: Annotated[str, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> dict:
    """Get task summary with counts.

    Args:
        user_id: Authenticated user ID from JWT
        db: Database session

    Returns:
        Dictionary with task counts: total, pending, completed, overdue, due_today, due_tomorrow
    """
    tasks = await task_service.get_user_tasks(db, user_id)
    task_responses = [TaskResponse.model_validate(task) for task in tasks]

    total = len(task_responses)
    pending = sum(1 for t in task_responses if not t.completed)
    completed = sum(1 for t in task_responses if t.completed)
    overdue = sum(1 for t in task_responses if t.is_overdue)
    due_today = sum(1 for t in task_responses if t.is_due_today)

    # Calculate due_tomorrow
    from datetime import datetime, timedelta, timezone
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    due_tomorrow = sum(
        1
        for t in task_responses
        if t.due_date
        and not t.completed
        and (t.due_date.replace(tzinfo=timezone.utc) if t.due_date.tzinfo is None else t.due_date).date()
        == tomorrow
    )

    return {
        "total": total,
        "pending": pending,
        "completed": completed,
        "overdue": overdue,
        "due_today": due_today,
        "due_tomorrow": due_tomorrow,
    }


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: Annotated[str, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> TaskResponse:
    """Get a specific task by ID.

    Args:
        task_id: ID of the task to retrieve
        user_id: Authenticated user ID from JWT
        db: Database session

    Returns:
        Task details

    Raises:
        HTTPException: 404 if task not found or not owned by user
    """
    task = await task_service.get_task_by_id(db, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return TaskResponse.model_validate(task)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: Annotated[str, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> TaskResponse:
    """Update a task.

    Args:
        task_id: ID of the task to update
        task_data: Task update data
        user_id: Authenticated user ID from JWT
        db: Database session

    Returns:
        Updated task

    Raises:
        HTTPException: 404 if task not found or not owned by user
    """
    task = await task_service.update_task(db, task_id, user_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return TaskResponse.model_validate(task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: Annotated[str, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    """Delete a task.

    Args:
        task_id: ID of the task to delete
        user_id: Authenticated user ID from JWT
        db: Database session

    Raises:
        HTTPException: 404 if task not found or not owned by user
    """
    success = await task_service.delete_task(db, task_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete(
    task_id: int,
    completed: bool,
    user_id: Annotated[str, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> TaskResponse:
    """Toggle task completion status.

    Args:
        task_id: ID of the task
        completed: New completion status
        user_id: Authenticated user ID from JWT
        db: Database session

    Returns:
        Updated task

    Raises:
        HTTPException: 404 if task not found or not owned by user
    """
    task = await task_service.toggle_task_complete(db, task_id, user_id, completed)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return TaskResponse.model_validate(task)
