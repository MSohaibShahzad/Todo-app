"""Unit tests for task sorting functionality (Phase-2 US4)."""

import pytest
from datetime import datetime, timedelta
from src.services.task_manager import TaskManager


@pytest.fixture
def manager_with_sortable_tasks():
    """Provide TaskManager with tasks suitable for sorting tests."""
    manager = TaskManager()

    # Add tasks with different priorities (high, medium, low, None)
    task1 = manager.add_task("Fix critical bug", "Production down", priority="high", category="Work")
    task2 = manager.add_task("Write documentation", "API docs needed", priority="medium", category="Work")
    task3 = manager.add_task("Update README", "Add installation instructions", priority="low", category="Work")
    task4 = manager.add_task("Buy groceries", "Milk and eggs")  # No priority (None)

    # Add tasks with alphabetically different titles
    task5 = manager.add_task("Alpha task", priority="medium", category="Test")
    task6 = manager.add_task("Zebra task", priority="medium", category="Test")
    task7 = manager.add_task("Beta task", priority="medium", category="Test")

    # Manually set due dates on tasks (bypassing add_task for now)
    today = datetime.now()
    task8 = manager.add_task("Urgent deadline", priority="high")
    task8.due_date = today + timedelta(days=1)

    task9 = manager.add_task("Future task", priority="low")
    task9.due_date = today + timedelta(days=30)

    task10 = manager.add_task("Medium deadline", priority="medium")
    task10.due_date = today + timedelta(days=7)

    task11 = manager.add_task("No deadline task", priority="medium")  # No due date

    return manager


# US4: Sort Tasks Tests

class TestSortTasksByPriority:
    """Tests for sort_tasks() by priority."""

    def test_sort_tasks_by_priority_high_to_low(self, manager_with_sortable_tasks):
        """Test sorting by priority: high > medium > low > None."""
        results = manager_with_sortable_tasks.sort_tasks(sort_by="priority")

        # Group tasks by priority
        high_tasks = [t for t in results if t.priority == "high"]
        medium_tasks = [t for t in results if t.priority == "medium"]
        low_tasks = [t for t in results if t.priority == "low"]
        none_tasks = [t for t in results if t.priority is None]

        # Verify counts
        assert len(high_tasks) == 2
        assert len(medium_tasks) == 6
        assert len(low_tasks) == 2
        assert len(none_tasks) == 1

        # Verify order: high first, then medium, then low, then None
        all_high_indices = [results.index(t) for t in high_tasks]
        all_medium_indices = [results.index(t) for t in medium_tasks]
        all_low_indices = [results.index(t) for t in low_tasks]
        all_none_indices = [results.index(t) for t in none_tasks]

        # All high priority tasks should come before all medium
        assert max(all_high_indices) < min(all_medium_indices)
        # All medium priority tasks should come before all low
        assert max(all_medium_indices) < min(all_low_indices)
        # All low priority tasks should come before all None
        assert max(all_low_indices) < min(all_none_indices)

    def test_sort_tasks_by_priority_with_ties_uses_id(self, manager_with_sortable_tasks):
        """Test that ties in priority are broken by ID (ascending)."""
        results = manager_with_sortable_tasks.sort_tasks(sort_by="priority")

        # Among high priority tasks, lower ID comes first
        high_priority_tasks = [t for t in results if t.priority == "high"]
        assert high_priority_tasks[0].id < high_priority_tasks[1].id


class TestSortTasksByTitle:
    """Tests for sort_tasks() by title (alphabetical)."""

    def test_sort_tasks_by_title_alphabetical(self, manager_with_sortable_tasks):
        """Test sorting by title alphabetically (A-Z)."""
        results = manager_with_sortable_tasks.sort_tasks(sort_by="title")

        # Check first few are alphabetically ordered
        assert results[0].title.lower() < results[1].title.lower()
        assert results[1].title.lower() < results[2].title.lower()

        # Specific checks for known titles
        alpha_task = next(t for t in results if t.title == "Alpha task")
        beta_task = next(t for t in results if t.title == "Beta task")
        zebra_task = next(t for t in results if t.title == "Zebra task")

        alpha_index = results.index(alpha_task)
        beta_index = results.index(beta_task)
        zebra_index = results.index(zebra_task)

        assert alpha_index < beta_index < zebra_index

    def test_sort_tasks_by_title_case_insensitive(self, manager_with_sortable_tasks):
        """Test that title sorting is case-insensitive."""
        # Add tasks with different cases
        manager_with_sortable_tasks.add_task("aardvark")
        manager_with_sortable_tasks.add_task("AARDVARK2")

        results = manager_with_sortable_tasks.sort_tasks(sort_by="title")

        aardvark = next(t for t in results if t.title == "aardvark")
        aardvark2 = next(t for t in results if t.title == "AARDVARK2")

        # Both should be early in the list
        assert results.index(aardvark) < 5
        assert results.index(aardvark2) < 5


class TestSortTasksByDueDate:
    """Tests for sort_tasks() by due_date."""

    def test_sort_tasks_by_due_date_soonest_first(self, manager_with_sortable_tasks):
        """Test sorting by due date (soonest first)."""
        results = manager_with_sortable_tasks.sort_tasks(sort_by="due_date")

        # Find tasks with due dates
        tasks_with_dates = [t for t in results if t.due_date is not None]

        # Should be sorted soonest to latest
        for i in range(len(tasks_with_dates) - 1):
            assert tasks_with_dates[i].due_date <= tasks_with_dates[i + 1].due_date

    def test_sort_tasks_by_due_date_none_values_last(self, manager_with_sortable_tasks):
        """Test that tasks without due dates appear last when sorting by due_date."""
        results = manager_with_sortable_tasks.sort_tasks(sort_by="due_date")

        # Count tasks with and without due dates
        tasks_with_dates = [t for t in results if t.due_date is not None]
        tasks_without_dates = [t for t in results if t.due_date is None]

        # All tasks with dates should come before tasks without dates
        last_with_date_index = results.index(tasks_with_dates[-1])
        first_without_date_index = results.index(tasks_without_dates[0])

        assert last_with_date_index < first_without_date_index


class TestSortTasksById:
    """Tests for sort_tasks() by ID (default)."""

    def test_sort_tasks_by_id_ascending(self, manager_with_sortable_tasks):
        """Test sorting by ID (creation order)."""
        results = manager_with_sortable_tasks.sort_tasks(sort_by="id")

        # Should be in ascending ID order
        for i in range(len(results) - 1):
            assert results[i].id < results[i + 1].id

    def test_sort_tasks_default_is_by_id(self, manager_with_sortable_tasks):
        """Test that default sorting (no sort_by) uses ID."""
        results_default = manager_with_sortable_tasks.sort_tasks()
        results_by_id = manager_with_sortable_tasks.sort_tasks(sort_by="id")

        assert results_default == results_by_id


class TestSortTasksEdgeCases:
    """Tests for edge cases in sorting."""

    def test_sort_tasks_empty_list(self):
        """Test sorting empty task list."""
        manager = TaskManager()
        results = manager.sort_tasks(sort_by="priority")

        assert results == []
        assert isinstance(results, list)

    def test_sort_tasks_single_task(self):
        """Test sorting single task."""
        manager = TaskManager()
        manager.add_task("Only task", priority="medium")

        results = manager.sort_tasks(sort_by="priority")

        assert len(results) == 1
        assert results[0].title == "Only task"
