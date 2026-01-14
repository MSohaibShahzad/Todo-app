"""Integration tests for full user workflows."""

from src.services.task_manager import TaskManager


def test_add_and_view_workflow():
    """Test complete add and view workflow (User Story 1).

    Integration test covering:
    - Add task with title and description
    - View task list
    - Verify task appears with correct details and status
    """
    manager = TaskManager()

    # Add first task
    task1 = manager.add_task("Buy groceries", "Milk, eggs, bread")
    assert task1.id == 1
    assert task1.is_complete is False

    # Add second task with empty description
    task2 = manager.add_task("Write report", "")
    assert task2.id == 2

    # View all tasks
    tasks = manager.get_all_tasks()
    assert len(tasks) == 2

    # Verify first task details
    assert tasks[0].id == 1
    assert tasks[0].title == "Buy groceries"
    assert tasks[0].description == "Milk, eggs, bread"
    assert tasks[0].is_complete is False

    # Verify second task details
    assert tasks[1].id == 2
    assert tasks[1].title == "Write report"
    assert tasks[1].description == ""
    assert tasks[1].is_complete is False


def test_empty_list_workflow():
    """Test viewing empty task list returns appropriate empty list."""
    manager = TaskManager()

    tasks = manager.get_all_tasks()

    assert tasks == []
    assert len(tasks) == 0


def test_empty_list_display_message():
    """Test that empty task list displays helpful message."""
    from src.cli.display import format_task_list

    manager = TaskManager()
    tasks = manager.get_all_tasks()
    formatted = format_task_list(tasks)

    assert "No tasks found" in formatted
    assert "Add a task to get started" in formatted


def test_mark_complete_workflow():
    """Test complete mark complete/incomplete workflow (User Story 2).

    Integration test covering:
    - Add tasks
    - Mark task as complete
    - View tasks to verify status change
    - Mark task as incomplete
    - Verify status indicators work correctly
    """
    manager = TaskManager()

    # Add tasks
    task1 = manager.add_task("Buy groceries", "Milk, eggs")
    task2 = manager.add_task("Write report", "Q4 summary")

    # Initially both incomplete
    assert task1.is_complete is False
    assert task2.is_complete is False

    # Mark first task as complete
    completed = manager.mark_complete(task1.id, True)
    assert completed.is_complete is True

    # View all tasks - verify first is complete, second is incomplete
    tasks = manager.get_all_tasks()
    assert tasks[0].is_complete is True
    assert tasks[1].is_complete is False

    # Mark first task back to incomplete
    incomplete = manager.mark_complete(task1.id, False)
    assert incomplete.is_complete is False

    # Verify both are now incomplete
    tasks = manager.get_all_tasks()
    assert tasks[0].is_complete is False
    assert tasks[1].is_complete is False
