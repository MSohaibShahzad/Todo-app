"""Integration test for complete Phase-2 workflow."""

import pytest
from src.services.task_manager import TaskManager


def test_complete_user_workflow():
    """Test complete workflow: add → categorize → prioritize → filter → search → sort → complete."""
    manager = TaskManager()

    # Step 1: Add tasks
    task1 = manager.add_task(
        "Write quarterly report",
        "Financial analysis for Q4",
        priority="high",
        category="Work"
    )
    task2 = manager.add_task(
        "Buy groceries",
        "Milk, eggs, bread",
        priority="medium",
        category="Personal"
    )
    task3 = manager.add_task(
        "Schedule dentist",
        "Annual checkup",
        priority="low",
        category="Health"
    )
    task4 = manager.add_task(
        "Review pull requests",
        "Code review needed",
        priority="high",
        category="Work"
    )

    # Verify all tasks created
    all_tasks = manager.get_all_tasks()
    assert len(all_tasks) == 4

    # Step 2: Update a task (change priority and category)
    updated_task = manager.update_task(
        task3.id,
        title="Schedule dentist appointment",
        priority="medium",
        category="Personal"
    )
    assert updated_task.priority == "medium"
    assert updated_task.category == "Personal"
    assert updated_task.title == "Schedule dentist appointment"

    # Step 3: Filter by category
    work_tasks = manager.filter_tasks(category="Work")
    assert len(work_tasks) == 2
    assert all(t.category == "Work" for t in work_tasks)

    # Step 4: Filter by priority
    high_priority = manager.filter_tasks(priority="high")
    assert len(high_priority) == 2
    assert all(t.priority == "high" for t in high_priority)

    # Step 5: Filter with multiple criteria (AND logic)
    high_work = manager.filter_tasks(priority="high", category="Work")
    assert len(high_work) == 2
    assert all(t.priority == "high" and t.category == "Work" for t in high_work)

    # Step 6: Search by keyword
    report_tasks = manager.search_tasks("report")
    assert len(report_tasks) == 1
    assert "report" in report_tasks[0].title.lower()

    # Step 7: Sort by priority
    sorted_by_priority = manager.sort_tasks(sort_by="priority")
    # High priority should come first
    assert sorted_by_priority[0].priority == "high"
    assert sorted_by_priority[1].priority == "high"
    # Medium in the middle
    assert sorted_by_priority[2].priority == "medium"
    assert sorted_by_priority[3].priority == "medium"

    # Step 8: Sort by title
    sorted_by_title = manager.sort_tasks(sort_by="title")
    titles = [t.title for t in sorted_by_title]
    # Verify alphabetical order
    assert titles == sorted(titles, key=str.lower)

    # Step 9: Mark tasks complete
    manager.mark_complete(task1.id, True)
    manager.mark_complete(task4.id, True)

    # Verify completion status
    completed_tasks = manager.filter_tasks(is_complete=True)
    assert len(completed_tasks) == 2
    assert task1.id in [t.id for t in completed_tasks]
    assert task4.id in [t.id for t in completed_tasks]

    # Step 10: Filter incomplete tasks
    incomplete_tasks = manager.filter_tasks(is_complete=False)
    assert len(incomplete_tasks) == 2

    # Step 11: Delete a task
    manager.delete_task(task2.id)
    remaining_tasks = manager.get_all_tasks()
    assert len(remaining_tasks) == 3
    assert task2.id not in [t.id for t in remaining_tasks]

    # Step 12: Verify final state
    final_tasks = manager.get_all_tasks()
    assert len(final_tasks) == 3
    # Verify we can still filter, search, and sort
    assert len(manager.filter_tasks(priority="high", is_complete=True)) == 2
    assert len(manager.search_tasks("dentist")) == 1
    assert len(manager.sort_tasks(sort_by="priority")) == 3


def test_workflow_with_edge_cases():
    """Test workflow with edge cases and boundary conditions."""
    manager = TaskManager()

    # Add task with all optional fields as None/default
    task1 = manager.add_task("Minimal task")
    assert task1.priority is None
    assert task1.category == "General"  # Default category
    assert task1.description == ""
    assert task1.is_complete is False

    # Search with no matches
    assert manager.search_tasks("nonexistent") == []

    # Filter with no matches
    assert manager.filter_tasks(priority="high") == []

    # Sort empty list
    empty_manager = TaskManager()
    assert empty_manager.sort_tasks(sort_by="priority") == []

    # Update task with only one field
    updated = manager.update_task(task1.id, priority="low")
    assert updated.priority == "low"
    assert updated.title == "Minimal task"  # Unchanged

    # Filter with all criteria matching
    task2 = manager.add_task("Test", priority="high", category="Work")
    manager.mark_complete(task2.id, True)
    
    exact_match = manager.filter_tasks(
        priority="high",
        category="Work",
        is_complete=True
    )
    assert len(exact_match) == 1
    assert exact_match[0].id == task2.id
