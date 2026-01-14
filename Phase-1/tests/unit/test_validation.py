"""Unit tests for input validation (Phase-2)."""

import pytest
from datetime import datetime, timedelta
from src.services.task_manager import TaskManager


@pytest.fixture
def empty_manager():
    """Provide fresh TaskManager for each test."""
    return TaskManager()


# US1: Priority Validation Tests

class TestPriorityValidation:
    """Tests for priority field validation."""

    def test_add_task_with_invalid_priority_raises_error(self, empty_manager):
        """Test that invalid priority raises ValueError."""
        with pytest.raises(ValueError, match="Priority must be one of"):
            empty_manager.add_task("Test task", priority="urgent")

    def test_add_task_with_empty_priority_raises_error(self, empty_manager):
        """Test that empty string priority raises ValueError."""
        with pytest.raises(ValueError, match="Priority must be one of"):
            empty_manager.add_task("Test task", priority="")

    def test_add_task_with_numeric_priority_raises_error(self, empty_manager):
        """Test that numeric priority raises ValueError."""
        with pytest.raises(ValueError, match="Priority must be one of"):
            empty_manager.add_task("Test task", priority="1")

    def test_add_task_with_case_sensitive_priority_raises_error(self, empty_manager):
        """Test that priority is case-sensitive."""
        with pytest.raises(ValueError, match="Priority must be one of"):
            empty_manager.add_task("Test task", priority="High")

        with pytest.raises(ValueError, match="Priority must be one of"):
            empty_manager.add_task("Test task", priority="MEDIUM")


# US2: Category Validation Tests

class TestCategoryValidation:
    """Tests for category field validation."""

    def test_add_task_with_category_exceeding_max_length_raises_error(self, empty_manager):
        """Test that category exceeding 50 chars raises ValueError."""
        long_category = "A" * 51
        with pytest.raises(ValueError, match="Category exceeds maximum length of 50"):
            empty_manager.add_task("Test task", category=long_category)

    def test_add_task_with_whitespace_only_category_raises_error(self, empty_manager):
        """Test that whitespace-only category raises ValueError."""
        with pytest.raises(ValueError, match="Category cannot be empty or whitespace"):
            empty_manager.add_task("Test task", category="   ")

    def test_add_task_with_empty_string_category_raises_error(self, empty_manager):
        """Test that empty string category raises ValueError."""
        with pytest.raises(ValueError, match="Category cannot be empty or whitespace"):
            empty_manager.add_task("Test task", category="")

    def test_update_task_with_invalid_category_raises_error(self, empty_manager):
        """Test that update_task with invalid category raises ValueError."""
        task = empty_manager.add_task("Test task", category="Work")

        # Test max length
        long_category = "B" * 51
        with pytest.raises(ValueError, match="Category exceeds maximum length of 50"):
            empty_manager.update_task(task.id, category=long_category)

        # Test whitespace
        with pytest.raises(ValueError, match="Category cannot be empty or whitespace"):
            empty_manager.update_task(task.id, category="   ")


# US5: Due Date Validation Tests

class TestDueDateValidation:
    """Tests for due_date field validation."""

    def test_add_task_with_past_due_date_raises_error(self, empty_manager):
        """Test that past due_date raises ValueError."""
        past_date = datetime.now() - timedelta(days=1)
        with pytest.raises(ValueError, match="Due date must be in the future"):
            empty_manager.add_task("Test task", due_date=past_date)

    def test_update_task_with_past_due_date_raises_error(self, empty_manager):
        """Test that updating to past due_date raises ValueError."""
        task = empty_manager.add_task("Test task")
        past_date = datetime.now() - timedelta(days=1)

        with pytest.raises(ValueError, match="Due date must be in the future"):
            empty_manager.update_task(task.id, due_date=past_date)


# US6: Recurrence Rule Validation Tests

class TestRecurrenceRuleValidation:
    """Tests for recurrence_rule field validation."""

    def test_add_task_with_invalid_recurrence_rule_raises_error(self, empty_manager):
        """Test that invalid recurrence_rule raises ValueError."""
        with pytest.raises(ValueError, match="Recurrence rule must be one of"):
            empty_manager.add_task("Test task", recurrence_rule="yearly")

    def test_add_task_with_empty_recurrence_rule_raises_error(self, empty_manager):
        """Test that empty string recurrence_rule raises ValueError."""
        with pytest.raises(ValueError, match="Recurrence rule must be one of"):
            empty_manager.add_task("Test task", recurrence_rule="")

    def test_add_task_with_case_sensitive_recurrence_rule_raises_error(self, empty_manager):
        """Test that recurrence_rule is case-sensitive."""
        with pytest.raises(ValueError, match="Recurrence rule must be one of"):
            empty_manager.add_task("Test task", recurrence_rule="Daily")
