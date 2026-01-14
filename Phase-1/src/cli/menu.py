"""Menu and input handling for console interface."""

from typing import Optional
from datetime import datetime
from src.services.task_manager import TaskManager, VALID_PRIORITIES, DEFAULT_CATEGORY, MAX_CATEGORY_LENGTH, VALID_RECURRENCE_RULES
from src.cli.display import format_task_list


def get_integer_input(prompt: str) -> int:
    """Get validated integer input from user.

    Args:
        prompt: Message to display to user

    Returns:
        int: Validated integer value
    """
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_string_input(prompt: str, allow_empty: bool = False, max_length: Optional[int] = None) -> str:
    """Get validated string input from user.

    Args:
        prompt: Message to display to user
        allow_empty: Whether empty string is valid (default False)
        max_length: Maximum allowed length (None = no limit)

    Returns:
        str: Validated string (whitespace stripped)
    """
    while True:
        value = input(prompt).strip()

        if not allow_empty and not value:
            print("Input cannot be empty.")
            continue

        if max_length and len(value) > max_length:
            print(f"Input exceeds maximum length of {max_length}.")
            continue

        return value


def get_priority_input() -> Optional[str]:
    """Get validated priority input from user.

    Returns:
        Optional[str]: Priority value ("low"|"medium"|"high") or None if skipped
    """
    print(f"Enter priority ({'/'.join(VALID_PRIORITIES)}) or press Enter to skip: ", end="")
    value = input().strip().lower()

    if not value:
        return None

    if value not in VALID_PRIORITIES:
        print(f"Invalid priority. Must be one of: {', '.join(VALID_PRIORITIES)}")
        return get_priority_input()

    return value


def get_category_input() -> Optional[str]:
    """Get validated category input from user.

    Returns:
        Optional[str]: Category value or None to use default "General"
    """
    print(f"Enter category (or press Enter for '{DEFAULT_CATEGORY}'): ", end="")
    value = input().strip()

    if not value:
        return None

    if len(value) > MAX_CATEGORY_LENGTH:
        print(f"Category too long. Maximum {MAX_CATEGORY_LENGTH} characters.")
        return get_category_input()

    return value


def get_due_date_input() -> Optional[datetime]:
    """Get validated due date input from user.

    Returns:
        Optional[datetime]: Due date value or None if skipped
    """
    print("Enter due date (YYYY-MM-DD) or press Enter to skip: ", end="")
    value = input().strip()

    if not value:
        return None

    try:
        # Parse the date string
        due_date = datetime.strptime(value, "%Y-%m-%d")
        return due_date
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD (e.g., 2026-12-31)")
        return get_due_date_input()


def get_recurrence_rule_input() -> Optional[str]:
    """Get validated recurrence rule input from user.

    Returns:
        Optional[str]: Recurrence rule value ("daily"|"weekly"|"monthly") or None if skipped
    """
    print(f"Enter recurrence ({'/'.join(VALID_RECURRENCE_RULES)}) or press Enter to skip: ", end="")
    value = input().strip().lower()

    if not value:
        return None

    if value not in VALID_RECURRENCE_RULES:
        print(f"Invalid recurrence rule. Must be one of: {', '.join(VALID_RECURRENCE_RULES)}")
        return get_recurrence_rule_input()

    return value


def add_task_command(manager: TaskManager) -> None:
    """Handle add task user command.

    Args:
        manager: TaskManager instance to add task to
    """
    try:
        title = get_string_input("Enter title: ", allow_empty=False, max_length=200)
        description = get_string_input("Enter description (optional, press Enter to skip): ", allow_empty=True, max_length=1000)
        priority = get_priority_input()
        category = get_category_input()
        due_date = get_due_date_input()
        recurrence_rule = get_recurrence_rule_input()

        task = manager.add_task(title, description, priority=priority, category=category, due_date=due_date, recurrence_rule=recurrence_rule)
        print(f"✓ Task created successfully! ID: {task.id}")

    except ValueError as e:
        print(f"✗ Error: {e}")


def view_tasks_command(manager: TaskManager) -> None:
    """Handle view tasks user command.

    Args:
        manager: TaskManager instance to get tasks from
    """
    tasks = manager.get_all_tasks()
    formatted_list = format_task_list(tasks)
    print(formatted_list)


def mark_complete_command(manager: TaskManager) -> None:
    """Handle mark task complete user command.

    Args:
        manager: TaskManager instance to mark task in
    """
    try:
        task_id = get_integer_input("Enter task ID: ")
        manager.mark_complete(task_id, True)
        print("✓ Task marked as complete!")

    except ValueError as e:
        print(f"✗ Error: {e}")


def mark_incomplete_command(manager: TaskManager) -> None:
    """Handle mark task incomplete user command.

    Args:
        manager: TaskManager instance to mark task in
    """
    try:
        task_id = get_integer_input("Enter task ID: ")
        manager.mark_complete(task_id, False)
        print("✓ Task marked as incomplete!")

    except ValueError as e:
        print(f"✗ Error: {e}")


def update_task_command(manager: TaskManager) -> None:
    """Handle update task user command.

    Args:
        manager: TaskManager instance to update task in
    """
    try:
        task_id = get_integer_input("Enter task ID: ")

        print("Leave blank to keep current value")
        title = input("Enter new title (or press Enter to skip): ").strip()
        description = input("Enter new description (or press Enter to skip): ").strip()
        priority = get_priority_input()
        category = get_category_input()
        due_date = get_due_date_input()

        # Convert empty strings to None for the update_task method
        title_value = title if title else None
        description_value = description if description else None

        manager.update_task(task_id, title=title_value, description=description_value, priority=priority, category=category, due_date=due_date)
        print("✓ Task updated successfully!")

    except ValueError as e:
        print(f"✗ Error: {e}")


def delete_task_command(manager: TaskManager) -> None:
    """Handle delete task user command.

    Args:
        manager: TaskManager instance to delete task from
    """
    try:
        task_id = get_integer_input("Enter task ID: ")
        manager.delete_task(task_id)
        print("✓ Task deleted successfully!")

    except ValueError as e:
        print(f"✗ Error: {e}")


def search_tasks_command(manager: TaskManager) -> None:
    """Handle search tasks by keyword user command.

    Args:
        manager: TaskManager instance to search in
    """
    keyword = input("Enter search keyword: ").strip()

    if not keyword:
        print("✗ Search keyword cannot be empty.")
        return

    results = manager.search_tasks(keyword)
    formatted_list = format_task_list(results)

    print(f"\n--- Search Results for '{keyword}' ({len(results)} found) ---")
    print(formatted_list)


def filter_tasks_command(manager: TaskManager) -> None:
    """Handle filter tasks by criteria user command.

    Args:
        manager: TaskManager instance to filter
    """
    print("=== Filter Tasks ===")
    print("Leave blank to skip a filter")

    # Get filter criteria
    print("\nFilter by priority (low/medium/high) or press Enter to skip: ", end="")
    priority_input = input().strip().lower()
    priority = priority_input if priority_input in VALID_PRIORITIES else None

    category_input = input("Filter by category or press Enter to skip: ").strip()
    category = category_input if category_input else None

    print("Filter by status (complete/incomplete) or press Enter to skip: ", end="")
    status_input = input().strip().lower()
    is_complete = None
    if status_input == "complete":
        is_complete = True
    elif status_input == "incomplete":
        is_complete = False

    # Apply filters
    results = manager.filter_tasks(priority=priority, category=category, is_complete=is_complete)

    # Build filter description
    filters_applied = []
    if priority:
        filters_applied.append(f"Priority={priority}")
    if category:
        filters_applied.append(f"Category={category}")
    if is_complete is not None:
        status_str = "Complete" if is_complete else "Incomplete"
        filters_applied.append(f"Status={status_str}")

    filter_desc = ", ".join(filters_applied) if filters_applied else "None (showing all)"

    formatted_list = format_task_list(results)
    print(f"\n--- Filtered Results ({len(results)} found) ---")
    print(f"Filters: {filter_desc}")
    print(formatted_list)
