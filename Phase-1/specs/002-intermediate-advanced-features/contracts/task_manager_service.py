"""
Service Contract: TaskManager Extended API

This contract defines the interface for the TaskManager service with
intermediate and advanced features (Phase-2 extension).

Principles:
- Backward compatible with Phase-1 API
- All new parameters are optional with defaults
- Validation errors raise ValueError with clear messages
- Returns immutable results (List[Task] are new lists, not references)
"""

from datetime import datetime
from typing import Dict, List, Optional, Literal
from src.models.task import Task


# Type Aliases
PriorityLevel = Optional[Literal["low", "medium", "high"]]
RecurrenceRule = Optional[Literal["daily", "weekly", "monthly"]]
SortKey = Literal["id", "priority", "due_date", "title", "category"]


class TaskManagerContract:
    """Interface contract for TaskManager service (Phase-1 + Phase-2)."""

    # ===== PHASE-1 METHODS (Unchanged) =====

    def add_task(
        self,
        title: str,
        description: str = "",
        # Phase-2 extensions (optional, default None):
        priority: PriorityLevel = None,
        category: Optional[str] = None,
        due_date: Optional[datetime] = None,
        recurrence_rule: RecurrenceRule = None
    ) -> Task:
        """Add a new task to the manager.

        Args:
            title: Task summary (required, max 200 chars, non-empty after strip)
            description: Detailed information (optional, max 1000 chars)
            priority: Priority level (optional, "low"|"medium"|"high"|None)
            category: Category/project (optional, max 50 chars, alphanumeric)
            due_date: Task deadline (optional, must be future datetime)
            recurrence_rule: Recurrence pattern (optional, "daily"|"weekly"|"monthly"|None)

        Returns:
            Task: Newly created task with assigned ID and is_complete=False

        Raises:
            ValueError: If title is empty/whitespace-only
            ValueError: If title exceeds 200 characters
            ValueError: If description exceeds 1000 characters
            ValueError: If priority not in {"low", "medium", "high", None}
            ValueError: If category exceeds 50 characters or is whitespace-only
            ValueError: If due_date is not in the future
            ValueError: If recurrence_rule not in {"daily", "weekly", "monthly", None}

        Example:
            >>> task = manager.add_task(
            ...     title="Review PR",
            ...     priority="high",
            ...     category="Work",
            ...     due_date=datetime(2026, 1, 15, 17, 0)
            ... )
            >>> task.id
            1
        """
        ...

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks sorted by ID (creation order).

        Returns:
            List[Task]: All tasks in ascending ID order (empty list if no tasks)
                        Returns a NEW list (mutations won't affect storage)

        Example:
            >>> tasks = manager.get_all_tasks()
            >>> len(tasks)
            5
        """
        ...

    def mark_complete(self, task_id: int, is_complete: bool) -> Task:
        """Mark task as complete or incomplete.

        For recurring tasks (recurrence_rule != None):
        - Marks the original task as complete
        - Generates a new task instance with updated due_date
        - New task has same title, description, priority, category, recurrence_rule
        - New task has new ID and is_complete=False

        Args:
            task_id: ID of task to update
            is_complete: True for complete, False for incomplete

        Returns:
            Task: Updated task object (or original task if recurring)

        Raises:
            ValueError: If task_id not found

        Side Effects (Recurring Tasks Only):
            - Creates new task in storage
            - Increments next_id counter

        Example (Non-Recurring):
            >>> task = manager.mark_complete(task_id=1, is_complete=True)
            >>> task.is_complete
            True

        Example (Recurring):
            >>> original = manager.add_task("Daily standup", recurrence_rule="daily",
            ...                             due_date=datetime(2026, 1, 8, 9, 0))
            >>> original.id
            1
            >>> completed = manager.mark_complete(task_id=1, is_complete=True)
            >>> completed.is_complete
            True
            >>> all_tasks = manager.get_all_tasks()
            >>> len(all_tasks)  # Original + new recurring instance
            2
            >>> new_task = all_tasks[1]
            >>> new_task.id
            2
            >>> new_task.due_date
            datetime(2026, 1, 9, 9, 0)  # +1 day
        """
        ...

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        # Phase-2 extensions:
        priority: Optional[PriorityLevel] = None,
        category: Optional[str] = None,
        due_date: Optional[datetime] = None,
        recurrence_rule: Optional[RecurrenceRule] = None
    ) -> Task:
        """Update task fields (any combination of fields).

        Args:
            task_id: ID of task to update
            title: New title (optional, None = keep existing)
            description: New description (optional, None = keep existing)
            priority: New priority (optional, None = keep existing)
            category: New category (optional, None = keep existing)
            due_date: New due date (optional, None = keep existing)
            recurrence_rule: New recurrence rule (optional, None = keep existing)

        Returns:
            Task: Updated task object

        Raises:
            ValueError: If task_id not found
            ValueError: If ALL fields are None (no update requested)
            ValueError: If title is empty/whitespace-only
            ValueError: If title exceeds 200 characters
            ValueError: If description exceeds 1000 characters
            ValueError: If priority not in {"low", "medium", "high", None}
            ValueError: If category exceeds 50 characters
            ValueError: If due_date is not in the future

        Example:
            >>> task = manager.update_task(
            ...     task_id=1,
            ...     priority="high",
            ...     due_date=datetime(2026, 1, 20, 12, 0)
            ... )
            >>> task.priority
            "high"
        """
        ...

    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID.

        Args:
            task_id: ID of task to delete

        Raises:
            ValueError: If task_id not found

        Side Effects:
            - Removes task from storage
            - ID is NOT reused for future tasks

        Example:
            >>> manager.delete_task(task_id=1)
            >>> manager.get_all_tasks()
            []
        """
        ...

    # ===== PHASE-2 NEW METHODS =====

    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by keyword (case-insensitive).

        Searches in:
        - Task title
        - Task description

        Does NOT search:
        - Priority, category, dates, ID

        Args:
            query: Search keyword or phrase (case-insensitive)

        Returns:
            List[Task]: Tasks matching query, sorted by ID
                        Returns empty list if no matches
                        Returns NEW list (mutations won't affect storage)

        Example:
            >>> results = manager.search_tasks("meeting")
            >>> # Matches "Team Meeting" and "Prepare meeting notes"
            >>> len(results)
            2
        """
        ...

    def filter_tasks(
        self,
        is_complete: Optional[bool] = None,
        priority: PriorityLevel = None,
        category: Optional[str] = None
    ) -> List[Task]:
        """Filter tasks by criteria (AND logic for multiple filters).

        Args:
            is_complete: Filter by completion status (None = no filter)
            priority: Filter by priority level (None = no filter)
            category: Filter by category (None = no filter, case-sensitive exact match)

        Returns:
            List[Task]: Tasks matching ALL provided filters, sorted by ID
                        Returns all tasks if no filters provided
                        Returns empty list if no matches
                        Returns NEW list (mutations won't affect storage)

        Example:
            >>> # High priority incomplete tasks in Work category
            >>> tasks = manager.filter_tasks(
            ...     is_complete=False,
            ...     priority="high",
            ...     category="Work"
            ... )
        """
        ...

    def sort_tasks(
        self,
        tasks: List[Task],
        sort_by: SortKey = "id",
        reverse: bool = False
    ) -> List[Task]:
        """Sort tasks by specified key.

        Sort Keys:
        - "id": Creation order (default)
        - "priority": high > medium > low > None
        - "due_date": Earliest first, None last
        - "title": Alphabetical (case-insensitive)
        - "category": Alphabetical (case-insensitive), None last

        Args:
            tasks: List of tasks to sort
            sort_by: Sort key (default: "id")
            reverse: Reverse sort order (default: False)

        Returns:
            List[Task]: NEW sorted list (does not mutate input)

        Example:
            >>> tasks = manager.get_all_tasks()
            >>> sorted_tasks = manager.sort_tasks(tasks, sort_by="priority")
            >>> sorted_tasks[0].priority
            "high"
        """
        ...

    def get_overdue_tasks(self) -> List[Task]:
        """Get all tasks with due_date in the past.

        Returns:
            List[Task]: Overdue tasks sorted by due_date (earliest first)
                        Returns empty list if no overdue tasks
                        Returns NEW list

        Example:
            >>> overdue = manager.get_overdue_tasks()
            >>> all(task.due_date < datetime.now() for task in overdue)
            True
        """
        ...

    def get_tasks_due_today(self) -> List[Task]:
        """Get all tasks with due_date.date() == today's date.

        Returns:
            List[Task]: Tasks due today, sorted by due time
                        Returns empty list if no tasks due today
                        Returns NEW list

        Example:
            >>> due_today = manager.get_tasks_due_today()
            >>> all(task.due_date.date() == datetime.now().date() for task in due_today)
            True
        """
        ...

    def get_upcoming_tasks(self, days: int = 3) -> List[Task]:
        """Get all tasks due within the next N days (excluding today).

        Args:
            days: Number of days to look ahead (default: 3)

        Returns:
            List[Task]: Upcoming tasks sorted by due_date
                        Returns empty list if no upcoming tasks
                        Returns NEW list

        Example:
            >>> upcoming = manager.get_upcoming_tasks(days=7)
            >>> # Tasks due in next 7 days (excluding today and overdue)
        """
        ...


# ===== VALIDATION CONSTANTS =====

MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000
MAX_CATEGORY_LENGTH = 50

VALID_PRIORITIES = {"low", "medium", "high"}
VALID_RECURRENCE_RULES = {"daily", "weekly", "monthly"}
VALID_SORT_KEYS = {"id", "priority", "due_date", "title", "category"}


# ===== ERROR MESSAGE TEMPLATES =====

ERROR_MESSAGES = {
    "task_not_found": "Task not found: {task_id}",
    "empty_title": "Title cannot be empty",
    "title_too_long": "Title exceeds maximum length of {max} characters",
    "description_too_long": "Description exceeds maximum length of {max} characters",
    "invalid_priority": "Priority must be one of {valid} or None",
    "category_too_long": "Category exceeds maximum length of {max} characters",
    "empty_category": "Category cannot be empty or whitespace-only",
    "due_date_past": "Due date must be in the future",
    "invalid_recurrence": "Recurrence rule must be one of {valid} or None",
    "no_update_fields": "Must provide at least one field to update",
    "invalid_sort_key": "Sort key must be one of {valid}",
}
