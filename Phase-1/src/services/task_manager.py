"""TaskManager service for managing tasks in memory."""

from typing import Dict, List, Optional
from src.models.task import Task


# Constants for validation
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000
INITIAL_TASK_ID = 1


class TaskManager:
    """Manages in-memory task storage and operations.

    Responsibilities:
    - Store tasks in memory (Dict[int, Task])
    - Assign unique sequential IDs to tasks
    - Validate task data (title/description length, non-empty title)
    - Provide CRUD operations (Create, Read, Update, Delete)
    - Manage task completion status

    Storage:
    - tasks: Dict[int, Task] - ID to Task mapping
    - next_id: int - Counter for sequential ID assignment (starts at 1)
    """

    def __init__(self) -> None:
        """Initialize empty TaskManager with no tasks."""
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = INITIAL_TASK_ID

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task to the manager.

        Args:
            title: Task summary (required, max 200 characters)
            description: Detailed information (optional, max 1000 characters)

        Returns:
            Task: Newly created task with assigned ID and is_complete=False

        Raises:
            ValueError: If title is empty/whitespace-only
            ValueError: If title exceeds 200 characters
            ValueError: If description exceeds 1000 characters
        """
        # Strip whitespace and validate title
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty")

        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError(f"Title exceeds maximum length of {MAX_TITLE_LENGTH} characters")

        # Validate description length
        if len(description) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Description exceeds maximum length of {MAX_DESCRIPTION_LENGTH} characters")

        # Create task with next available ID
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            is_complete=False
        )

        # Store task and increment ID counter
        self.tasks[self.next_id] = task
        self.next_id += 1

        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks sorted by ID (creation order).

        Returns:
            List[Task]: All tasks in ascending ID order (empty list if no tasks)
        """
        # Return tasks sorted by ID
        return sorted(self.tasks.values(), key=lambda t: t.id)

    def mark_complete(self, task_id: int, is_complete: bool) -> Task:
        """Mark task as complete or incomplete.

        Args:
            task_id: ID of task to update
            is_complete: True for complete, False for incomplete

        Returns:
            Task: Updated task object

        Raises:
            ValueError: If task_id not found
        """
        # Check if task exists
        if task_id not in self.tasks:
            raise ValueError(f"Task not found: {task_id}")

        # Update task status
        task = self.tasks[task_id]
        task.is_complete = is_complete

        return task

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        """Update task title and/or description.

        Args:
            task_id: ID of task to update
            title: New title (optional, None = keep existing)
            description: New description (optional, None = keep existing)

        Returns:
            Task: Updated task object

        Raises:
            ValueError: If task_id not found
            ValueError: If neither title nor description provided
            ValueError: If title is empty/whitespace-only
            ValueError: If title exceeds 200 characters
            ValueError: If description exceeds 1000 characters
        """
        # Check if task exists
        if task_id not in self.tasks:
            raise ValueError(f"Task not found: {task_id}")

        # Ensure at least one field is provided
        if title is None and description is None:
            raise ValueError("Must provide at least one field to update")

        task = self.tasks[task_id]

        # Update title if provided
        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Title cannot be empty")
            if len(title) > MAX_TITLE_LENGTH:
                raise ValueError(f"Title exceeds maximum length of {MAX_TITLE_LENGTH} characters")
            task.title = title

        # Update description if provided
        if description is not None:
            if len(description) > MAX_DESCRIPTION_LENGTH:
                raise ValueError(f"Description exceeds maximum length of {MAX_DESCRIPTION_LENGTH} characters")
            task.description = description

        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID.

        Args:
            task_id: ID of task to delete

        Raises:
            ValueError: If task_id not found
        """
        # Check if task exists
        if task_id not in self.tasks:
            raise ValueError(f"Task not found: {task_id}")

        # Remove task from storage
        del self.tasks[task_id]
