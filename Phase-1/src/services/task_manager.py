"""TaskManager service for managing tasks in memory."""

from typing import Dict, List, Optional
from datetime import datetime
from src.models.task import Task


# Constants for validation
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000
INITIAL_TASK_ID = 1

# Phase-2: Priority validation
VALID_PRIORITIES = ["low", "medium", "high"]

# Phase-2: Category validation
MAX_CATEGORY_LENGTH = 50
DEFAULT_CATEGORY = "General"

# Phase-2: Recurrence validation
VALID_RECURRENCE_RULES = ["daily", "weekly", "monthly"]


def validate_priority(priority: Optional[str]) -> None:
    """Validate priority value.

    Args:
        priority: Priority value to validate (or None)

    Raises:
        ValueError: If priority is not None and not in VALID_PRIORITIES
    """
    if priority is not None and priority not in VALID_PRIORITIES:
        raise ValueError(f"Priority must be one of {VALID_PRIORITIES}, got: {priority}")


def validate_category(category: Optional[str]) -> None:
    """Validate category value.

    Args:
        category: Category value to validate (or None)

    Raises:
        ValueError: If category is empty/whitespace or exceeds MAX_CATEGORY_LENGTH
    """
    if category is not None:
        if not category.strip():
            raise ValueError("Category cannot be empty or whitespace")
        if len(category) > MAX_CATEGORY_LENGTH:
            raise ValueError(f"Category exceeds maximum length of {MAX_CATEGORY_LENGTH} characters")


def validate_due_date(due_date: Optional[datetime]) -> None:
    """Validate due_date value.

    Args:
        due_date: Due date value to validate (or None)

    Raises:
        ValueError: If due_date is in the past (before today)
    """
    if due_date is not None:
        # Compare dates only (ignore time component)
        # Allow today's date, but not past dates
        now = datetime.now()
        if due_date.date() < now.date():
            raise ValueError("Due date must be in the future")


def validate_recurrence_rule(recurrence_rule: Optional[str]) -> None:
    """Validate recurrence_rule value.

    Args:
        recurrence_rule: Recurrence rule value to validate (or None)

    Raises:
        ValueError: If recurrence_rule is not None and not in VALID_RECURRENCE_RULES
    """
    if recurrence_rule is not None and recurrence_rule not in VALID_RECURRENCE_RULES:
        raise ValueError(f"Recurrence rule must be one of {VALID_RECURRENCE_RULES}, got: {recurrence_rule}")


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

    def _calculate_next_due_date(self, current_due_date: datetime, recurrence_rule: str) -> datetime:
        """Calculate next due date based on recurrence rule.

        Args:
            current_due_date: Current due date of the task
            recurrence_rule: Recurrence rule ("daily"|"weekly"|"monthly")

        Returns:
            datetime: Next due date based on recurrence rule
        """
        from datetime import timedelta
        from calendar import monthrange

        if recurrence_rule == "daily":
            return current_due_date + timedelta(days=1)
        elif recurrence_rule == "weekly":
            return current_due_date + timedelta(weeks=1)
        elif recurrence_rule == "monthly":
            # Handle monthly recurrence with edge case for end of month
            year = current_due_date.year
            month = current_due_date.month
            day = current_due_date.day

            # Calculate next month
            if month == 12:
                next_year = year + 1
                next_month = 1
            else:
                next_year = year
                next_month = month + 1

            # Get the last day of the next month
            last_day_of_next_month = monthrange(next_year, next_month)[1]

            # Use the same day, or last day if original day doesn't exist in next month
            next_day = min(day, last_day_of_next_month)

            return current_due_date.replace(year=next_year, month=next_month, day=next_day)
        else:
            # Should not reach here due to validation, but return current date as fallback
            return current_due_date

    def add_task(self, title: str, description: str = "", priority: Optional[str] = None, category: Optional[str] = None, due_date: Optional[datetime] = None, recurrence_rule: Optional[str] = None) -> Task:
        """Add a new task to the manager.

        Args:
            title: Task summary (required, max 200 characters)
            description: Detailed information (optional, max 1000 characters)
            priority: Task priority (optional, "low"|"medium"|"high")
            category: Task category (optional, defaults to "General", max 50 characters)
            due_date: Task due date (optional, must be in the future)
            recurrence_rule: Task recurrence rule (optional, "daily"|"weekly"|"monthly")

        Returns:
            Task: Newly created task with assigned ID and is_complete=False

        Raises:
            ValueError: If title is empty/whitespace-only
            ValueError: If title exceeds 200 characters
            ValueError: If description exceeds 1000 characters
            ValueError: If priority is not None and not in VALID_PRIORITIES
            ValueError: If category is empty/whitespace or exceeds MAX_CATEGORY_LENGTH
            ValueError: If due_date is in the past
            ValueError: If recurrence_rule is not None and not in VALID_RECURRENCE_RULES
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

        # Validate priority
        validate_priority(priority)

        # Validate and default category
        validate_category(category)
        if category is None:
            category = DEFAULT_CATEGORY

        # Validate due_date
        validate_due_date(due_date)

        # Validate recurrence_rule
        validate_recurrence_rule(recurrence_rule)

        # Create task with next available ID
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            is_complete=False,
            priority=priority,
            category=category,
            due_date=due_date,
            recurrence_rule=recurrence_rule
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

        For recurring tasks: when marked complete (True), creates a new instance
        with the next due date based on the recurrence rule.

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

        # If marking as complete and task has recurrence rule, create new instance
        if is_complete and task.recurrence_rule and task.due_date:
            # Calculate next due date
            next_due_date = self._calculate_next_due_date(task.due_date, task.recurrence_rule)

            # Create new instance of the recurring task
            self.add_task(
                title=task.title,
                description=task.description,
                priority=task.priority,
                category=task.category,
                due_date=next_due_date,
                recurrence_rule=task.recurrence_rule
            )

        return task

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None, category: Optional[str] = None, due_date: Optional[datetime] = None) -> Task:
        """Update task title and/or description and/or priority and/or category and/or due_date.

        Args:
            task_id: ID of task to update
            title: New title (optional, None = keep existing)
            description: New description (optional, None = keep existing)
            priority: New priority (optional, None = keep existing, "low"|"medium"|"high")
            category: New category (optional, None = keep existing, max 50 characters)
            due_date: New due date (optional, None = keep existing, must be in the future)

        Returns:
            Task: Updated task object

        Raises:
            ValueError: If task_id not found
            ValueError: If no fields provided
            ValueError: If title is empty/whitespace-only
            ValueError: If title exceeds 200 characters
            ValueError: If description exceeds 1000 characters
            ValueError: If priority is not None and not in VALID_PRIORITIES
            ValueError: If category is empty/whitespace or exceeds MAX_CATEGORY_LENGTH
            ValueError: If due_date is in the past
        """
        # Check if task exists
        if task_id not in self.tasks:
            raise ValueError(f"Task not found: {task_id}")

        # Ensure at least one field is provided
        if title is None and description is None and priority is None and category is None and due_date is None:
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

        # Update priority if provided
        if priority is not None:
            validate_priority(priority)
            task.priority = priority

        # Update category if provided
        if category is not None:
            validate_category(category)
            task.category = category

        # Update due_date if provided
        if due_date is not None:
            validate_due_date(due_date)
            task.due_date = due_date

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

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in title or description (case-insensitive).

        Args:
            keyword: Search keyword to match against title and description

        Returns:
            List[Task]: Tasks matching the keyword, sorted by ID
        """
        keyword_lower = keyword.lower()
        matching_tasks = []

        for task in self.get_all_tasks():
            # Case-insensitive search in title and description
            if keyword_lower in task.title.lower() or keyword_lower in task.description.lower():
                matching_tasks.append(task)

        return matching_tasks

    def filter_tasks(
        self,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        is_complete: Optional[bool] = None
    ) -> List[Task]:
        """Filter tasks by priority, category, and/or completion status.

        Uses AND logic: all specified criteria must match.

        Args:
            priority: Filter by priority ("low"|"medium"|"high", None = no filter)
            category: Filter by category (None = no filter)
            is_complete: Filter by completion status (True/False/None = no filter)

        Returns:
            List[Task]: Tasks matching all specified criteria, sorted by ID
        """
        matching_tasks = []

        for task in self.get_all_tasks():
            # Check priority filter
            if priority is not None and task.priority != priority:
                continue

            # Check category filter
            if category is not None and task.category != category:
                continue

            # Check completion status filter
            if is_complete is not None and task.is_complete != is_complete:
                continue

            # All filters passed
            matching_tasks.append(task)

        return matching_tasks

    def sort_tasks(self, sort_by: str = "id") -> List[Task]:
        """Sort tasks by specified key.

        Args:
            sort_by: Sort key ("id"|"priority"|"title"|"due_date", default "id")

        Returns:
            List[Task]: Tasks sorted by specified key, with secondary sort by ID for ties

        Sorting rules:
            - priority: high > medium > low > None (tasks with no priority last)
            - title: Alphabetical A-Z (case-insensitive)
            - due_date: Soonest first, None values last
            - id: Ascending order (default)
        """
        tasks = self.get_all_tasks()

        if sort_by == "priority":
            # Define priority order: high=0, medium=1, low=2, None=3
            priority_order = {"high": 0, "medium": 1, "low": 2}

            def priority_key(task):
                return (priority_order.get(task.priority, 3), task.id)

            return sorted(tasks, key=priority_key)

        elif sort_by == "title":
            # Sort alphabetically by title (case-insensitive), then by ID
            return sorted(tasks, key=lambda task: (task.title.lower(), task.id))

        elif sort_by == "due_date":
            # Sort by due date (soonest first), None values last, then by ID
            def due_date_key(task):
                if task.due_date is None:
                    # Use a far future date for None values to sort them last
                    from datetime import datetime
                    return (datetime.max, task.id)
                return (task.due_date, task.id)

            return sorted(tasks, key=due_date_key)

        else:  # sort_by == "id" or any other value defaults to ID
            # Already sorted by ID in get_all_tasks(), but explicit for clarity
            return sorted(tasks, key=lambda task: task.id)

    def get_overdue_tasks(self) -> List[Task]:
        """Get all incomplete tasks with due_date in the past.

        Returns:
            List[Task]: Incomplete tasks with past due dates, sorted by ID
        """
        now = datetime.now()
        overdue_tasks = []

        for task in self.get_all_tasks():
            # Only include incomplete tasks with a due date in the past
            if not task.is_complete and task.due_date is not None:
                if task.due_date.date() < now.date():
                    overdue_tasks.append(task)

        return overdue_tasks

    def get_tasks_due_today(self) -> List[Task]:
        """Get all tasks with due_date today.

        Returns:
            List[Task]: Tasks due today, sorted by ID
        """
        now = datetime.now()
        today_tasks = []

        for task in self.get_all_tasks():
            # Include tasks with due date matching today
            if task.due_date is not None:
                if task.due_date.date() == now.date():
                    today_tasks.append(task)

        return today_tasks

    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Get all tasks due in the next N days (excluding today and overdue).

        Args:
            days: Number of days to look ahead (default: 7)

        Returns:
            List[Task]: Tasks due in the next N days, sorted by ID
        """
        from datetime import timedelta

        now = datetime.now()
        today = now.date()
        end_date = (now + timedelta(days=days)).date()

        upcoming_tasks = []

        for task in self.get_all_tasks():
            # Include tasks with due date between tomorrow and end_date
            if task.due_date is not None:
                task_date = task.due_date.date()
                if today < task_date <= end_date:
                    upcoming_tasks.append(task)

        return upcoming_tasks
