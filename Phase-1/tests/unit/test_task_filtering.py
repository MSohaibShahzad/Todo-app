"""Unit tests for search and filter functionality (Phase-2 US3)."""

import pytest
from src.services.task_manager import TaskManager


@pytest.fixture
def manager_with_sample_tasks():
    """Provide TaskManager with diverse sample tasks."""
    manager = TaskManager()
    # High priority work tasks
    manager.add_task("Write report", "Quarterly financial report", priority="high", category="Work")
    manager.add_task("Fix bug in login", "Authentication error", priority="high", category="Work")

    # Medium priority personal tasks
    manager.add_task("Buy groceries", "Milk, eggs, bread", priority="medium", category="Personal")
    manager.add_task("Call dentist", "Schedule appointment", priority="medium", category="Personal")

    # Low priority shopping tasks
    manager.add_task("Order books", "Python programming books", priority="low", category="Shopping")
    manager.add_task("Buy gift", "Birthday gift for mom", priority="low", category="Shopping")

    # No priority general tasks
    manager.add_task("Read news", "", category="General")
    manager.add_task("Water plants", "Indoor plants need watering")  # Uses default General category

    # Mark some as complete
    manager.mark_complete(1, True)  # Write report - complete
    manager.mark_complete(3, True)  # Buy groceries - complete
    manager.mark_complete(7, True)  # Read news - complete

    return manager


# US3: Search Tasks Tests

class TestSearchTasks:
    """Tests for search_tasks() method."""

    def test_search_tasks_by_title(self, manager_with_sample_tasks):
        """Test searching tasks by title keyword."""
        results = manager_with_sample_tasks.search_tasks("buy")

        assert len(results) == 2
        assert results[0].title == "Buy groceries"
        assert results[1].title == "Buy gift"

    def test_search_tasks_by_description(self, manager_with_sample_tasks):
        """Test searching tasks by description keyword."""
        results = manager_with_sample_tasks.search_tasks("appointment")

        assert len(results) == 1
        assert results[0].title == "Call dentist"

    def test_search_tasks_case_insensitive(self, manager_with_sample_tasks):
        """Test search is case-insensitive."""
        results_lower = manager_with_sample_tasks.search_tasks("python")
        results_upper = manager_with_sample_tasks.search_tasks("PYTHON")
        results_mixed = manager_with_sample_tasks.search_tasks("PyThOn")

        assert len(results_lower) == 1
        assert len(results_upper) == 1
        assert len(results_mixed) == 1
        assert results_lower[0].title == "Order books"
        assert results_upper[0].title == "Order books"
        assert results_mixed[0].title == "Order books"

    def test_search_tasks_no_matches(self, manager_with_sample_tasks):
        """Test search returns empty list when no matches."""
        results = manager_with_sample_tasks.search_tasks("nonexistent")

        assert results == []
        assert isinstance(results, list)

    def test_search_tasks_partial_match(self, manager_with_sample_tasks):
        """Test search matches partial keywords."""
        results = manager_with_sample_tasks.search_tasks("repo")

        assert len(results) == 1
        assert results[0].title == "Write report"


# US3: Filter Tasks Tests

class TestFilterTasks:
    """Tests for filter_tasks() method."""

    def test_filter_tasks_by_priority_high(self, manager_with_sample_tasks):
        """Test filtering tasks by high priority."""
        results = manager_with_sample_tasks.filter_tasks(priority="high")

        assert len(results) == 2
        assert all(task.priority == "high" for task in results)

    def test_filter_tasks_by_priority_low(self, manager_with_sample_tasks):
        """Test filtering tasks by low priority."""
        results = manager_with_sample_tasks.filter_tasks(priority="low")

        assert len(results) == 2
        assert all(task.priority == "low" for task in results)

    def test_filter_tasks_by_category_work(self, manager_with_sample_tasks):
        """Test filtering tasks by Work category."""
        results = manager_with_sample_tasks.filter_tasks(category="Work")

        assert len(results) == 2
        assert all(task.category == "Work" for task in results)

    def test_filter_tasks_by_category_personal(self, manager_with_sample_tasks):
        """Test filtering tasks by Personal category."""
        results = manager_with_sample_tasks.filter_tasks(category="Personal")

        assert len(results) == 2
        assert all(task.category == "Personal" for task in results)

    def test_filter_tasks_by_status_complete(self, manager_with_sample_tasks):
        """Test filtering tasks by completion status (complete)."""
        results = manager_with_sample_tasks.filter_tasks(is_complete=True)

        assert len(results) == 3
        assert all(task.is_complete is True for task in results)

    def test_filter_tasks_by_status_incomplete(self, manager_with_sample_tasks):
        """Test filtering tasks by completion status (incomplete)."""
        results = manager_with_sample_tasks.filter_tasks(is_complete=False)

        assert len(results) == 5
        assert all(task.is_complete is False for task in results)

    def test_filter_tasks_multiple_criteria_and_logic(self, manager_with_sample_tasks):
        """Test filtering with multiple criteria uses AND logic."""
        # Filter: high priority AND Work category AND incomplete
        results = manager_with_sample_tasks.filter_tasks(
            priority="high",
            category="Work",
            is_complete=False
        )

        assert len(results) == 1
        assert results[0].title == "Fix bug in login"
        assert results[0].priority == "high"
        assert results[0].category == "Work"
        assert results[0].is_complete is False

    def test_filter_tasks_no_criteria_returns_all(self, manager_with_sample_tasks):
        """Test filter with no criteria returns all tasks."""
        results = manager_with_sample_tasks.filter_tasks()

        assert len(results) == 8
        assert results == manager_with_sample_tasks.get_all_tasks()

    def test_filter_tasks_no_matches(self, manager_with_sample_tasks):
        """Test filter returns empty list when no matches."""
        # No tasks with high priority AND Shopping category
        results = manager_with_sample_tasks.filter_tasks(priority="high", category="Shopping")

        assert results == []
        assert isinstance(results, list)
