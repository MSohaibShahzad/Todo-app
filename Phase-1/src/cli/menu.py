"""Menu and input handling for console interface."""

from typing import Optional
from src.services.task_manager import TaskManager
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


def add_task_command(manager: TaskManager) -> None:
    """Handle add task user command.

    Args:
        manager: TaskManager instance to add task to
    """
    try:
        title = get_string_input("Enter title: ", allow_empty=False, max_length=200)
        description = get_string_input("Enter description (optional, press Enter to skip): ", allow_empty=True, max_length=1000)

        task = manager.add_task(title, description)
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

        # Convert empty strings to None for the update_task method
        title_value = title if title else None
        description_value = description if description else None

        manager.update_task(task_id, title=title_value, description=description_value)
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
