"""Display formatting helpers for console output."""

from typing import List
from datetime import datetime
from src.models.task import Task


def format_status_indicator(is_complete: bool) -> str:
    """Get status indicator symbol.

    Args:
        is_complete: Task completion status

    Returns:
        str: "☑" if complete, "☐" if incomplete
    """
    return "☑" if is_complete else "☐"


def format_priority_badge(priority: str) -> str:
    """Get colored priority badge.

    Args:
        priority: Priority level ("low"|"medium"|"high"|None)

    Returns:
        str: Colored priority badge or empty string if None
    """
    if not priority:
        return ""

    # Color codes: Red for high, Yellow for medium, Blue for low
    colors = {
        "high": "\033[91m",    # Red
        "medium": "\033[93m",  # Yellow
        "low": "\033[94m"      # Blue
    }
    reset = "\033[0m"

    color = colors.get(priority, "")
    return f"{color}[{priority.upper()}]{reset}"


def format_due_date_indicator(due_date: datetime) -> str:
    """Get colored due date indicator.

    Args:
        due_date: Task due date or None

    Returns:
        str: Colored due date indicator or empty string if None

        Indicators:
        - "OVERDUE" (red, bold) if past due
        - "DUE TODAY" (yellow, bold) if due today
        - "Due: YYYY-MM-DD" (normal) if future
    """
    if not due_date:
        return ""

    now = datetime.now()
    today = now.date()
    task_date = due_date.date()

    # Color codes
    red_bold = "\033[91m\033[1m"
    yellow_bold = "\033[93m\033[1m"
    reset = "\033[0m"

    if task_date < today:
        return f"{red_bold}OVERDUE{reset}"
    elif task_date == today:
        return f"{yellow_bold}DUE TODAY{reset}"
    else:
        return f"Due: {task_date.strftime('%Y-%m-%d')}"


def format_task_list(tasks: List[Task]) -> str:
    """Format task list for console display.

    Args:
        tasks: List of Task objects to format

    Returns:
        str: Formatted string ready for printing

    Format:
        === Task List ===
        [1] ☐ [HIGH] Title [OVERDUE]
            Category: Work | Description: text
        [2] ☑ [MEDIUM] Title [DUE TODAY]
            Category: Personal
        [3] ☐ Title Due: 2026-12-31
            Category: General | Description: text
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
            priority_badge = format_priority_badge(task.priority)
            due_date_indicator = format_due_date_indicator(task.due_date)

            # Build title line with optional priority badge and due date
            title_parts = [f"[{task.id}]", status]
            if priority_badge:
                title_parts.append(priority_badge)
            title_parts.append(task.title)
            if due_date_indicator:
                title_parts.append(due_date_indicator)

            lines.append(" ".join(title_parts))

            # Build metadata line (category, description, and recurrence)
            metadata_parts = []
            if task.category:
                metadata_parts.append(f"Category: {task.category}")
            if task.description:
                metadata_parts.append(f"Description: {task.description}")
            if task.recurrence_rule:
                metadata_parts.append(f"Recurring: {task.recurrence_rule}")

            if metadata_parts:
                lines.append(f"    {' | '.join(metadata_parts)}")

    lines.append("=== End of List ===")
    return "\n".join(lines)
