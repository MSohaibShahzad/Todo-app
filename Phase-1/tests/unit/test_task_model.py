"""Unit tests for Task model."""

from datetime import datetime
from src.models.task import Task


def test_task_creation_with_all_fields():
    """Test Task dataclass creation with all fields provided."""
    task = Task(id=1, title="Buy groceries", description="Milk, eggs, bread", is_complete=False)

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.is_complete is False


def test_task_creation_with_defaults():
    """Test Task dataclass creation with default values for optional fields."""
    task = Task(id=1, title="Buy groceries")

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == ""
    assert task.is_complete is False


def test_task_completion_status_can_be_set():
    """Test Task completion status can be set to True."""
    task = Task(id=1, title="Test task", is_complete=True)

    assert task.is_complete is True


# Phase-2 Tests

def test_task_with_priority():
    """Test task creation with priority field."""
    task = Task(id=1, title="Test", priority="high")
    assert task.priority == "high"


def test_task_with_category():
    """Test task creation with category field."""
    task = Task(id=1, title="Test", category="Work")
    assert task.category == "Work"


def test_task_with_due_date():
    """Test task creation with due date."""
    due = datetime(2026, 1, 15, 12, 0)
    task = Task(id=1, title="Test", due_date=due)
    assert task.due_date == due


def test_task_with_recurrence_rule():
    """Test task creation with recurrence rule."""
    task = Task(id=1, title="Test", recurrence_rule="daily")
    assert task.recurrence_rule == "daily"


def test_task_defaults_for_phase2_fields():
    """Test that Phase-2 fields default to None."""
    task = Task(id=1, title="Test")
    assert task.priority is None
    assert task.category is None
    assert task.due_date is None
    assert task.recurrence_rule is None
