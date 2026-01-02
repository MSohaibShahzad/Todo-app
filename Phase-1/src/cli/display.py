"""Display formatting helpers for console output."""

from typing import List
from src.models.task import Task


def format_status_indicator(is_complete: bool) -> str:
    """Get status indicator symbol.

    Args:
        is_complete: Task completion status

    Returns:
        str: "☑" if complete, "☐" if incomplete
    """
    return "☑" if is_complete else "☐"


def format_task_list(tasks: List[Task]) -> str:
    """Format task list for console display.

    Args:
        tasks: List of Task objects to format

    Returns:
        str: Formatted string ready for printing

    Format:
        === Task List ===
        [1] ☐ Title
            Description: text
        [2] ☑ Title
            Description: text
        === End of List ===

        Or if empty:
        === Task List ===
        No tasks found. Add a task to get started!
        === End of List ===
    """
    lines = ["=== Task List ==="]

    if not tasks:
        lines.append("No tasks found. Add a task to get started!")
    else:
        for task in tasks:
            status = format_status_indicator(task.is_complete)
            lines.append(f"[{task.id}] {status} {task.title}")
            if task.description:
                lines.append(f"    Description: {task.description}")

    lines.append("=== End of List ===")
    return "\n".join(lines)
