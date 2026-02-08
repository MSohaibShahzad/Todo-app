"""MCP server for todo task operations.

This module exposes task management operations as MCP tools for AI agents.
All tools are stateless and persist data through the database.
"""
from datetime import datetime
from typing import Any, Optional, List
from mcp.types import TextContent
from sqlmodel import select, or_, col

from src.models.task import Priority, Task
from src.schemas.task import TaskCreate, TaskUpdate
from src.services import task_service
from src.mcp.utils import get_db_session


async def find_task_by_title_or_id(
    user_id: str,
    task_identifier: str
) -> Optional[Task]:
    """Find a task by ID or title.

    Args:
        user_id: ID of the user
        task_identifier: Either a task ID (number) or task title (text)

    Returns:
        Task if found, None otherwise

    Raises:
        ValueError: If multiple tasks match the title
    """
    async with get_db_session() as db:
        # Try to parse as integer ID first
        try:
            task_id = int(task_identifier)
            task = await task_service.get_task_by_id(db, task_id, user_id)
            return task
        except (ValueError, TypeError):
            # Not an ID, search by title
            pass

        # Search by title (case-insensitive partial match)
        result = await db.execute(
            select(Task)
            .where(
                Task.user_id == user_id,
                col(Task.title).ilike(f"%{task_identifier}%")
            )
            .order_by(Task.created_at.desc())
        )
        tasks = result.scalars().all()

        if not tasks:
            return None

        if len(tasks) > 1:
            task_list = [f"ID {t.id}: {t.title}" for t in tasks[:5]]
            raise ValueError(
                f"Multiple tasks found matching '{task_identifier}':\n" +
                "\n".join(task_list) +
                "\nPlease specify the task ID or be more specific."
            )

        return tasks[0]


async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    category: Optional[str] = None,
    due_date: Optional[str] = None
) -> TextContent:
    """Add a new task to the user's todo list.

    Args:
        user_id: ID of the user creating the task
        title: Task title (required, 1-255 characters)
        description: Optional task description
        priority: Task priority (low, medium, high). Default: medium
        category: Optional category for task organization
        due_date: Optional due date in ISO 8601 format (e.g., "2026-01-16T14:00:00Z")

    Returns:
        TextContent with success message and task ID

    Raises:
        ValueError: If validation fails (empty title, invalid priority, invalid date format)
    """
    # Validate title
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty")

    # Validate priority
    valid_priorities = {"low", "medium", "high"}
    priority_lower = priority.lower()
    if priority_lower not in valid_priorities:
        raise ValueError(f"Invalid priority '{priority}'. Must be one of: {', '.join(valid_priorities)}")

    # Parse and validate due_date
    parsed_due_date: Optional[datetime] = None
    if due_date:
        try:
            parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Invalid date format '{due_date}'. Expected ISO 8601 format (e.g., '2026-01-16T14:00:00Z')") from e

    # Create task using service layer
    async with get_db_session() as db:
        task_data = TaskCreate(
            title=title.strip(),
            description=description.strip() if description else None,
            priority=Priority(priority_lower),
            category=category.strip() if category else None,
            due_date=parsed_due_date
        )

        task = await task_service.create_task(db, user_id, task_data)

        return TextContent(
            type="text",
            text=f"Task created successfully! Task ID: {task.id}, Title: '{task.title}'"
        )


async def list_tasks(
    user_id: str,
    filter_completed: Optional[bool] = None,
    filter_priority: Optional[str] = None,
    filter_category: Optional[str] = None,
    limit: int = 50
) -> TextContent:
    """List user's tasks with optional filters.

    Args:
        user_id: ID of the user
        filter_completed: Filter by completion status (True/False/None for all)
        filter_priority: Filter by priority (low, medium, high)
        filter_category: Filter by category name
        limit: Maximum number of tasks to return (default: 50, max: 100)

    Returns:
        TextContent with formatted task list
    """
    # Validate limit
    if limit < 1 or limit > 100:
        raise ValueError("Limit must be between 1 and 100")

    async with get_db_session() as db:
        tasks = await task_service.get_user_tasks(db, user_id)

        # Apply filters
        filtered_tasks = tasks
        if filter_completed is not None:
            filtered_tasks = [t for t in filtered_tasks if t.completed == filter_completed]
        if filter_priority:
            filtered_tasks = [t for t in filtered_tasks if t.priority.value == filter_priority.lower()]
        if filter_category:
            filtered_tasks = [t for t in filtered_tasks if t.category and t.category.lower() == filter_category.lower()]

        # Apply limit
        filtered_tasks = filtered_tasks[:limit]

        if not filtered_tasks:
            return TextContent(
                type="text",
                text="No tasks found matching your criteria."
            )

        # Format tasks
        task_list = []
        for task in filtered_tasks:
            status = "✓" if task.completed else "○"
            due_info = f", Due: {task.due_date.strftime('%Y-%m-%d')}" if task.due_date else ""
            cat_info = f", Category: {task.category}" if task.category else ""
            task_list.append(
                f"{status} [{task.id}] {task.title} (Priority: {task.priority.value}{due_info}{cat_info})"
            )

        return TextContent(
            type="text",
            text=f"Found {len(filtered_tasks)} task(s):\n" + "\n".join(task_list)
        )


async def update_task(
    user_id: str,
    task_identifier: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    due_date: Optional[str] = None,
    completed: Optional[bool] = None
) -> TextContent:
    """Update an existing task.

    Args:
        user_id: ID of the user
        task_identifier: Task ID (number) or task title (text) to identify the task
        title: New title (optional)
        description: New description (optional)
        priority: New priority (low, medium, high) (optional)
        category: New category (optional)
        due_date: New due date in ISO 8601 format (optional)
        completed: New completion status (optional)

    Returns:
        TextContent with success message

    Raises:
        ValueError: If task not found or validation fails
    """
    # Find the task by ID or title
    task = await find_task_by_title_or_id(user_id, task_identifier)
    if not task:
        raise ValueError(f"Task '{task_identifier}' not found")

    # Validate priority if provided
    if priority:
        valid_priorities = {"low", "medium", "high"}
        priority_lower = priority.lower()
        if priority_lower not in valid_priorities:
            raise ValueError(f"Invalid priority '{priority}'. Must be one of: {', '.join(valid_priorities)}")

    # Parse due_date if provided
    parsed_due_date: Optional[datetime] = None
    if due_date:
        try:
            parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Invalid date format '{due_date}'. Expected ISO 8601 format") from e

    async with get_db_session() as db:
        # Build update data
        update_data = TaskUpdate(
            title=title.strip() if title else None,
            description=description.strip() if description else None,
            priority=Priority(priority.lower()) if priority else None,
            category=category.strip() if category else None,
            due_date=parsed_due_date,
            completed=completed
        )

        updated_task = await task_service.update_task(db, task.id, user_id, update_data)

        if not updated_task:
            raise ValueError(f"Failed to update task '{task_identifier}'")

        return TextContent(
            type="text",
            text=f"Task updated successfully! Task ID: {updated_task.id}, Title: '{updated_task.title}'"
        )


async def delete_task(
    user_id: str,
    task_identifier: str
) -> TextContent:
    """Delete a task.

    Args:
        user_id: ID of the user
        task_identifier: Task ID (number) or task title (text) to identify the task

    Returns:
        TextContent with success message

    Raises:
        ValueError: If task not found
    """
    # Find the task by ID or title
    task = await find_task_by_title_or_id(user_id, task_identifier)
    if not task:
        raise ValueError(f"Task '{task_identifier}' not found")

    async with get_db_session() as db:
        success = await task_service.delete_task(db, task.id, user_id)

        if not success:
            raise ValueError(f"Failed to delete task '{task_identifier}'")

        return TextContent(
            type="text",
            text=f"Task '{task.title}' (ID: {task.id}) deleted successfully!"
        )


async def mark_task_complete(
    user_id: str,
    task_identifier: str,
    completed: bool = True
) -> TextContent:
    """Mark a task as complete or incomplete.

    Args:
        user_id: ID of the user
        task_identifier: Task ID (number) or task title (text) to identify the task
        completed: Completion status (default: True)

    Returns:
        TextContent with success message

    Raises:
        ValueError: If task not found
    """
    # Find the task by ID or title
    task = await find_task_by_title_or_id(user_id, task_identifier)
    if not task:
        raise ValueError(f"Task '{task_identifier}' not found")

    async with get_db_session() as db:
        updated_task = await task_service.toggle_task_complete(db, task.id, user_id, completed)

        if not updated_task:
            raise ValueError(f"Failed to mark task '{task_identifier}' as {'complete' if completed else 'incomplete'}")

        status = "complete" if completed else "incomplete"
        return TextContent(
            type="text",
            text=f"Task {updated_task.id} marked as {status}! Title: '{updated_task.title}'"
        )


async def search_tasks(
    user_id: str,
    query: str,
    limit: int = 20
) -> TextContent:
    """Search tasks by keyword in title or description.

    Args:
        user_id: ID of the user
        query: Search query string
        limit: Maximum number of results (default: 20, max: 50)

    Returns:
        TextContent with search results

    Raises:
        ValueError: If query is empty
    """
    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")

    if limit < 1 or limit > 50:
        raise ValueError("Limit must be between 1 and 50")

    async with get_db_session() as db:
        query_lower = query.strip().lower()

        # Search in title and description
        result = await db.execute(
            select(Task)
            .where(
                Task.user_id == user_id,
                or_(
                    col(Task.title).ilike(f"%{query_lower}%"),
                    col(Task.description).ilike(f"%{query_lower}%")
                )
            )
            .order_by(Task.created_at.desc())
            .limit(limit)
        )
        tasks = result.scalars().all()

        if not tasks:
            return TextContent(
                type="text",
                text=f"No tasks found matching '{query}'"
            )

        # Format results
        task_list = []
        for task in tasks:
            status = "✓" if task.completed else "○"
            due_info = f", Due: {task.due_date.strftime('%Y-%m-%d')}" if task.due_date else ""
            task_list.append(
                f"{status} [{task.id}] {task.title} (Priority: {task.priority.value}{due_info})"
            )

        return TextContent(
            type="text",
            text=f"Found {len(tasks)} task(s) matching '{query}':\n" + "\n".join(task_list)
        )


async def bulk_delete_tasks(
    user_id: str,
    task_ids: List[int]
) -> TextContent:
    """Delete multiple tasks at once.

    Args:
        user_id: ID of the user
        task_ids: List of task IDs to delete

    Returns:
        TextContent with summary of deleted tasks

    Raises:
        ValueError: If task_ids is empty or exceeds limit
    """
    if not task_ids:
        raise ValueError("No task IDs provided")

    if len(task_ids) > 50:
        raise ValueError("Cannot delete more than 50 tasks at once")

    async with get_db_session() as db:
        deleted_count = 0
        failed_ids = []

        for task_id in task_ids:
            success = await task_service.delete_task(db, task_id, user_id)
            if success:
                deleted_count += 1
            else:
                failed_ids.append(task_id)

        result_msg = f"Successfully deleted {deleted_count} task(s)"
        if failed_ids:
            result_msg += f". Failed to delete tasks: {', '.join(map(str, failed_ids))} (not found or no permission)"

        return TextContent(
            type="text",
            text=result_msg
        )
