"""Unit tests for Task model."""

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
