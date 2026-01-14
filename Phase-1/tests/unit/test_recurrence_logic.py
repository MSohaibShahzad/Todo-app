"""Unit tests for recurring task logic (Phase-2 US6)."""

import pytest
from datetime import datetime, timedelta
from src.services.task_manager import TaskManager


@pytest.fixture
def empty_manager():
    """Provide fresh TaskManager for each test."""
    return TaskManager()


# US6: Recurring Task Tests

class TestMarkCompleteRecurrenceDaily:
    """Tests for mark_complete with daily recurrence."""

    def test_mark_complete_daily_creates_new_instance(self, empty_manager):
        """Test marking daily recurring task complete creates new instance for next day."""
        today = datetime.now()
        tomorrow = today + timedelta(days=1)

        # Create daily recurring task
        task = empty_manager.add_task(
            "Daily standup",
            due_date=today,
            recurrence_rule="daily"
        )
        assert task.recurrence_rule == "daily"
        assert task.due_date.date() == today.date()

        # Mark complete
        completed = empty_manager.mark_complete(task.id, True)
        assert completed.is_complete is True

        # Verify new instance created with next day's due date
        all_tasks = empty_manager.get_all_tasks()
        assert len(all_tasks) == 2

        # Find the new incomplete task
        new_task = [t for t in all_tasks if not t.is_complete][0]
        assert new_task.id != task.id
        assert new_task.title == "Daily standup"
        assert new_task.due_date.date() == tomorrow.date()
        assert new_task.recurrence_rule == "daily"


class TestMarkCompleteRecurrenceWeekly:
    """Tests for mark_complete with weekly recurrence."""

    def test_mark_complete_weekly_creates_new_instance(self, empty_manager):
        """Test marking weekly recurring task complete creates new instance for next week."""
        today = datetime.now()
        next_week = today + timedelta(weeks=1)

        # Create weekly recurring task
        task = empty_manager.add_task(
            "Weekly meeting",
            due_date=today,
            recurrence_rule="weekly"
        )

        # Mark complete
        empty_manager.mark_complete(task.id, True)

        # Verify new instance created with next week's due date
        all_tasks = empty_manager.get_all_tasks()
        assert len(all_tasks) == 2

        new_task = [t for t in all_tasks if not t.is_complete][0]
        assert new_task.title == "Weekly meeting"
        assert new_task.due_date.date() == next_week.date()
        assert new_task.recurrence_rule == "weekly"


class TestMarkCompleteRecurrenceMonthly:
    """Tests for mark_complete with monthly recurrence."""

    def test_mark_complete_monthly_creates_new_instance(self, empty_manager):
        """Test marking monthly recurring task complete creates new instance for next month."""
        # Use a specific date to test monthly recurrence
        from datetime import datetime
        current_date = datetime(2026, 1, 15)

        # Create monthly recurring task
        task = empty_manager.add_task(
            "Monthly report",
            due_date=current_date,
            recurrence_rule="monthly"
        )

        # Manually set due_date to current_date for testing
        task.due_date = current_date

        # Mark complete
        empty_manager.mark_complete(task.id, True)

        # Verify new instance created
        all_tasks = empty_manager.get_all_tasks()
        assert len(all_tasks) == 2

        new_task = [t for t in all_tasks if not t.is_complete][0]
        assert new_task.title == "Monthly report"
        # Should be same day next month (Feb 15)
        assert new_task.due_date.date() == datetime(2026, 2, 15).date()
        assert new_task.recurrence_rule == "monthly"

    def test_monthly_recurrence_edge_case_jan_31_to_feb_28(self, empty_manager):
        """Test monthly recurrence from Jan 31 creates Feb 28 (non-leap year)."""
        from datetime import datetime

        # Jan 31, 2026 (2026 is not a leap year)
        jan_31 = datetime(2026, 1, 31)

        task = empty_manager.add_task(
            "End of month task",
            due_date=jan_31,
            recurrence_rule="monthly"
        )

        # Manually set due_date for testing
        task.due_date = jan_31

        # Mark complete
        empty_manager.mark_complete(task.id, True)

        # Verify new instance has Feb 28 (last day of February in non-leap year)
        all_tasks = empty_manager.get_all_tasks()
        new_task = [t for t in all_tasks if not t.is_complete][0]

        # Feb only has 28 days in 2026
        assert new_task.due_date.date() == datetime(2026, 2, 28).date()

    def test_monthly_recurrence_edge_case_dec_to_jan_next_year(self, empty_manager):
        """Test monthly recurrence from December rolls over to January next year."""
        from datetime import datetime

        # Dec 15, 2026
        dec_15 = datetime(2026, 12, 15)

        task = empty_manager.add_task(
            "December task",
            due_date=dec_15,
            recurrence_rule="monthly"
        )

        # Manually set due_date for testing
        task.due_date = dec_15

        # Mark complete
        empty_manager.mark_complete(task.id, True)

        # Verify new instance has Jan 15, 2027 (next year)
        all_tasks = empty_manager.get_all_tasks()
        new_task = [t for t in all_tasks if not t.is_complete][0]

        assert new_task.due_date.date() == datetime(2027, 1, 15).date()


class TestMarkCompleteNonRecurring:
    """Tests for mark_complete with non-recurring tasks."""

    def test_mark_complete_non_recurring_no_new_instance(self, empty_manager):
        """Test marking non-recurring task complete does NOT create new instance."""
        today = datetime.now()

        # Create non-recurring task
        task = empty_manager.add_task("One-time task", due_date=today)
        assert task.recurrence_rule is None

        # Mark complete
        empty_manager.mark_complete(task.id, True)

        # Verify no new instance created
        all_tasks = empty_manager.get_all_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0].is_complete is True
