"""Unit tests for TaskManager service."""

import pytest
from datetime import datetime, timedelta
from src.services.task_manager import TaskManager, MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH


@pytest.fixture
def empty_manager():
    """Provide fresh TaskManager for each test."""
    return TaskManager()


@pytest.fixture
def manager_with_tasks():
    """Provide TaskManager pre-populated with sample tasks."""
    manager = TaskManager()
    manager.add_task("Task 1", "Description 1")
    manager.add_task("Task 2", "Description 2")
    return manager


class TestAddTask:
    """Tests for add_task() method."""

    def test_add_task_assigns_sequential_ids(self, empty_manager):
        """Test that add_task() assigns sequential IDs starting from 1."""
        task1 = empty_manager.add_task("First task", "First description")
        task2 = empty_manager.add_task("Second task", "Second description")

        assert task1.id == 1
        assert task2.id == 2

    def test_add_task_sets_title_and_description(self, empty_manager):
        """Test that add_task() correctly sets title and description."""
        task = empty_manager.add_task("Buy groceries", "Milk, eggs, bread")

        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"

    def test_add_task_sets_initial_status_incomplete(self, empty_manager):
        """Test that add_task() sets is_complete to False by default."""
        task = empty_manager.add_task("Test task", "")

        assert task.is_complete is False

    def test_add_task_allows_empty_description(self, empty_manager):
        """Test that add_task() allows empty string as description."""
        task = empty_manager.add_task("Title only", "")

        assert task.description == ""

    def test_add_task_rejects_empty_title(self, empty_manager):
        """Test that add_task() raises ValueError for empty title."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            empty_manager.add_task("", "Valid description")

        with pytest.raises(ValueError, match="Title cannot be empty"):
            empty_manager.add_task("   ", "Valid description")

    def test_add_task_rejects_title_exceeding_max_length(self, empty_manager):
        """Test that add_task() raises ValueError for title exceeding 200 chars."""
        long_title = "A" * (MAX_TITLE_LENGTH + 1)

        with pytest.raises(ValueError, match=f"Title exceeds maximum length of {MAX_TITLE_LENGTH}"):
            empty_manager.add_task(long_title, "")

    def test_add_task_rejects_description_exceeding_max_length(self, empty_manager):
        """Test that add_task() raises ValueError for description exceeding 1000 chars."""
        long_description = "B" * (MAX_DESCRIPTION_LENGTH + 1)

        with pytest.raises(ValueError, match=f"Description exceeds maximum length of {MAX_DESCRIPTION_LENGTH}"):
            empty_manager.add_task("Valid title", long_description)

    def test_add_task_with_very_long_title_1000_chars(self, empty_manager):
        """Test that add_task() rejects title with 1000+ characters."""
        very_long_title = "x" * 1000

        with pytest.raises(ValueError, match="Title exceeds maximum length"):
            empty_manager.add_task(very_long_title, "Description")

    def test_add_task_with_very_long_description_2000_chars(self, empty_manager):
        """Test that add_task() rejects description with 2000+ characters."""
        very_long_description = "x" * 2000

        with pytest.raises(ValueError, match="Description exceeds maximum length"):
            empty_manager.add_task("Title", very_long_description)


class TestGetAllTasks:
    """Tests for get_all_tasks() method."""

    def test_get_all_tasks_returns_empty_list_when_no_tasks(self, empty_manager):
        """Test that get_all_tasks() returns empty list when no tasks exist."""
        tasks = empty_manager.get_all_tasks()

        assert tasks == []
        assert isinstance(tasks, list)

    def test_get_all_tasks_returns_tasks_sorted_by_id(self, manager_with_tasks):
        """Test that get_all_tasks() returns tasks sorted by ID in ascending order."""
        tasks = manager_with_tasks.get_all_tasks()

        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[0].title == "Task 1"
        assert tasks[1].id == 2
        assert tasks[1].title == "Task 2"

    def test_get_all_tasks_reflects_added_tasks(self, empty_manager):
        """Test that get_all_tasks() reflects newly added tasks."""
        empty_manager.add_task("First", "")
        empty_manager.add_task("Second", "")
        empty_manager.add_task("Third", "")

        tasks = empty_manager.get_all_tasks()

        assert len(tasks) == 3
        assert [t.id for t in tasks] == [1, 2, 3]


class TestMarkComplete:
    """Tests for mark_complete() method."""

    def test_mark_complete_sets_status_to_true(self, manager_with_tasks):
        """Test that mark_complete() changes status to complete (True)."""
        task = manager_with_tasks.mark_complete(1, True)

        assert task.is_complete is True
        assert task.id == 1

        # Verify change persists in storage
        retrieved = manager_with_tasks.get_all_tasks()[0]
        assert retrieved.is_complete is True

    def test_mark_complete_sets_status_to_false(self, manager_with_tasks):
        """Test that mark_complete() can change status back to incomplete (False)."""
        # First mark as complete
        manager_with_tasks.mark_complete(1, True)

        # Then mark as incomplete
        task = manager_with_tasks.mark_complete(1, False)

        assert task.is_complete is False
        assert task.id == 1

        # Verify change persists
        retrieved = manager_with_tasks.get_all_tasks()[0]
        assert retrieved.is_complete is False

    def test_mark_complete_raises_error_for_non_existent_id(self, empty_manager):
        """Test that mark_complete() raises ValueError for non-existent task ID."""
        with pytest.raises(ValueError, match="Task not found: 999"):
            empty_manager.mark_complete(999, True)

    def test_mark_complete_is_idempotent(self, manager_with_tasks):
        """Test that marking a complete task as complete again works (idempotent)."""
        # Mark as complete twice
        manager_with_tasks.mark_complete(1, True)
        task = manager_with_tasks.mark_complete(1, True)

        # Should still be complete, no error
        assert task.is_complete is True

        # Mark as incomplete twice
        manager_with_tasks.mark_complete(1, False)
        task = manager_with_tasks.mark_complete(1, False)

        # Should still be incomplete, no error
        assert task.is_complete is False


class TestUpdateTask:
    """Tests for update_task() method."""

    def test_update_task_updates_title_only(self, manager_with_tasks):
        """Test that update_task() can update only the title."""
        task = manager_with_tasks.update_task(1, title="Updated Title")

        assert task.id == 1
        assert task.title == "Updated Title"
        assert task.description == "Description 1"  # Unchanged

        # Verify change persists in storage
        retrieved = manager_with_tasks.get_all_tasks()[0]
        assert retrieved.title == "Updated Title"
        assert retrieved.description == "Description 1"

    def test_update_task_updates_description_only(self, manager_with_tasks):
        """Test that update_task() can update only the description."""
        task = manager_with_tasks.update_task(1, description="Updated Description")

        assert task.id == 1
        assert task.title == "Task 1"  # Unchanged
        assert task.description == "Updated Description"

        # Verify change persists
        retrieved = manager_with_tasks.get_all_tasks()[0]
        assert retrieved.title == "Task 1"
        assert retrieved.description == "Updated Description"

    def test_update_task_updates_both_title_and_description(self, manager_with_tasks):
        """Test that update_task() can update both title and description."""
        task = manager_with_tasks.update_task(
            1,
            title="New Title",
            description="New Description"
        )

        assert task.id == 1
        assert task.title == "New Title"
        assert task.description == "New Description"

        # Verify changes persist
        retrieved = manager_with_tasks.get_all_tasks()[0]
        assert retrieved.title == "New Title"
        assert retrieved.description == "New Description"

    def test_update_task_raises_error_for_non_existent_id(self, empty_manager):
        """Test that update_task() raises ValueError for non-existent task ID."""
        with pytest.raises(ValueError, match="Task not found: 999"):
            empty_manager.update_task(999, title="New Title")

    def test_update_task_rejects_empty_title(self, manager_with_tasks):
        """Test that update_task() raises ValueError for empty title."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            manager_with_tasks.update_task(1, title="")

        with pytest.raises(ValueError, match="Title cannot be empty"):
            manager_with_tasks.update_task(1, title="   ")

    def test_update_task_rejects_title_exceeding_max_length(self, manager_with_tasks):
        """Test that update_task() raises ValueError for title exceeding 200 chars."""
        long_title = "A" * (MAX_TITLE_LENGTH + 1)

        with pytest.raises(ValueError, match=f"Title exceeds maximum length of {MAX_TITLE_LENGTH}"):
            manager_with_tasks.update_task(1, title=long_title)

    def test_update_task_rejects_description_exceeding_max_length(self, manager_with_tasks):
        """Test that update_task() raises ValueError for description exceeding 1000 chars."""
        long_description = "B" * (MAX_DESCRIPTION_LENGTH + 1)

        with pytest.raises(ValueError, match=f"Description exceeds maximum length of {MAX_DESCRIPTION_LENGTH}"):
            manager_with_tasks.update_task(1, description=long_description)

    def test_update_task_raises_error_when_no_fields_provided(self, manager_with_tasks):
        """Test that update_task() raises ValueError when neither title nor description is provided."""
        with pytest.raises(ValueError, match="Must provide at least one field to update"):
            manager_with_tasks.update_task(1)


class TestDeleteTask:
    """Tests for delete_task() method."""

    def test_delete_task_removes_task_from_storage(self, manager_with_tasks):
        """Test that delete_task() removes the task from storage."""
        # Verify task exists initially
        assert 1 in manager_with_tasks.tasks

        # Delete the task
        manager_with_tasks.delete_task(1)

        # Verify task is removed
        assert 1 not in manager_with_tasks.tasks
        tasks = manager_with_tasks.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 2

    def test_delete_task_does_not_affect_other_tasks(self, manager_with_tasks):
        """Test that delete_task() does not affect other tasks."""
        manager_with_tasks.delete_task(1)

        # Task 2 should still exist with original data
        tasks = manager_with_tasks.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 2
        assert tasks[0].title == "Task 2"
        assert tasks[0].description == "Description 2"

    def test_delete_task_raises_error_for_non_existent_id(self, empty_manager):
        """Test that delete_task() raises ValueError for non-existent task ID."""
        with pytest.raises(ValueError, match="Task not found: 999"):
            empty_manager.delete_task(999)

    def test_delete_task_can_delete_all_tasks(self, manager_with_tasks):
        """Test that delete_task() can delete all tasks leaving empty storage."""
        manager_with_tasks.delete_task(1)
        manager_with_tasks.delete_task(2)

        tasks = manager_with_tasks.get_all_tasks()
        assert tasks == []
        assert len(manager_with_tasks.tasks) == 0

    def test_delete_task_is_idempotent_for_errors(self, manager_with_tasks):
        """Test that deleting same task twice raises error on second attempt."""
        # First delete succeeds
        manager_with_tasks.delete_task(1)

        # Second delete raises error
        with pytest.raises(ValueError, match="Task not found: 1"):
            manager_with_tasks.delete_task(1)


# Phase-2 Tests: US1 - Task Prioritization

class TestAddTaskWithPriority:
    """Tests for add_task() with priority parameter (Phase-2)."""

    def test_add_task_with_valid_priority(self, empty_manager):
        """Test add_task() with valid priority."""
        task = empty_manager.add_task("Test task", priority="high")

        assert task.priority == "high"
        assert task.title == "Test task"

    def test_add_task_with_low_priority(self, empty_manager):
        """Test add_task() with low priority."""
        task = empty_manager.add_task("Low priority task", priority="low")
        assert task.priority == "low"

    def test_add_task_with_medium_priority(self, empty_manager):
        """Test add_task() with medium priority."""
        task = empty_manager.add_task("Medium priority task", priority="medium")
        assert task.priority == "medium"


class TestUpdateTaskPriority:
    """Tests for update_task() with priority parameter (Phase-2)."""

    def test_update_task_priority(self, empty_manager):
        """Test updating task priority."""
        task = empty_manager.add_task("Test task", priority="low")
        assert task.priority == "low"

        updated = empty_manager.update_task(task.id, priority="high")
        assert updated.priority == "high"

        # Verify persistence
        retrieved = empty_manager.get_all_tasks()[0]
        assert retrieved.priority == "high"


# Phase-2 Tests: US2 - Task Categorization

class TestAddTaskWithCategory:
    """Tests for add_task() with category parameter (Phase-2)."""

    def test_add_task_with_category(self, empty_manager):
        """Test add_task() with valid category."""
        task = empty_manager.add_task("Test task", category="Work")

        assert task.category == "Work"
        assert task.title == "Test task"

    def test_add_task_with_default_general_category(self, empty_manager):
        """Test add_task() defaults to 'General' category when not specified."""
        task = empty_manager.add_task("Test task")

        assert task.category == "General"

    def test_add_task_with_multiple_categories(self, empty_manager):
        """Test add_task() with different categories."""
        task1 = empty_manager.add_task("Work task", category="Work")
        task2 = empty_manager.add_task("Personal task", category="Personal")
        task3 = empty_manager.add_task("Shopping task", category="Shopping")

        assert task1.category == "Work"
        assert task2.category == "Personal"
        assert task3.category == "Shopping"


class TestUpdateTaskCategory:
    """Tests for update_task() with category parameter (Phase-2)."""

    def test_update_task_category(self, empty_manager):
        """Test updating task category."""
        task = empty_manager.add_task("Test task", category="Work")
        assert task.category == "Work"

        updated = empty_manager.update_task(task.id, category="Personal")
        assert updated.category == "Personal"

        # Verify persistence
        retrieved = empty_manager.get_all_tasks()[0]
        assert retrieved.category == "Personal"


# Phase-2 Tests: US5 - Due Dates and Reminders

class TestAddTaskWithDueDate:
    """Tests for add_task() with due_date parameter (Phase-2 US5)."""

    def test_add_task_with_due_date(self, empty_manager):
        """Test add_task() with valid future due_date."""
        future_date = datetime.now() + timedelta(days=3)
        task = empty_manager.add_task("Test task", due_date=future_date)

        assert task.due_date == future_date
        assert task.title == "Test task"

    def test_add_task_without_due_date_defaults_to_none(self, empty_manager):
        """Test add_task() defaults to None when due_date not specified."""
        task = empty_manager.add_task("Test task")

        assert task.due_date is None


class TestUpdateTaskDueDate:
    """Tests for update_task() with due_date parameter (Phase-2 US5)."""

    def test_update_task_due_date(self, empty_manager):
        """Test updating task due_date."""
        future_date = datetime.now() + timedelta(days=5)
        task = empty_manager.add_task("Test task")
        assert task.due_date is None

        updated = empty_manager.update_task(task.id, due_date=future_date)
        assert updated.due_date == future_date

        # Verify persistence
        retrieved = empty_manager.get_all_tasks()[0]
        assert retrieved.due_date == future_date


class TestGetOverdueTasks:
    """Tests for get_overdue_tasks() method (Phase-2 US5)."""

    def test_get_overdue_tasks_returns_past_due_tasks(self, empty_manager):
        """Test get_overdue_tasks() returns tasks with due_date in the past."""
        past_date = datetime.now() - timedelta(days=1)
        future_date = datetime.now() + timedelta(days=1)

        # Create task with future date first, then manually set to past for testing
        overdue = empty_manager.add_task("Overdue task", due_date=future_date)
        overdue.due_date = past_date  # Manually set to past for testing

        empty_manager.add_task("Future task", due_date=future_date)
        empty_manager.add_task("No due date task")

        result = empty_manager.get_overdue_tasks()

        assert len(result) == 1
        assert result[0].id == overdue.id

    def test_get_overdue_tasks_excludes_completed_tasks(self, empty_manager):
        """Test get_overdue_tasks() excludes completed tasks even if overdue."""
        past_date = datetime.now() - timedelta(days=1)
        future_date = datetime.now() + timedelta(days=1)

        # Create tasks with future date first, then manually set to past for testing
        overdue_incomplete = empty_manager.add_task("Overdue incomplete", due_date=future_date)
        overdue_incomplete.due_date = past_date  # Manually set to past for testing

        overdue_complete = empty_manager.add_task("Overdue complete", due_date=future_date)
        overdue_complete.due_date = past_date  # Manually set to past for testing
        empty_manager.mark_complete(overdue_complete.id, True)

        result = empty_manager.get_overdue_tasks()

        assert len(result) == 1
        assert result[0].id == overdue_incomplete.id


class TestGetTasksDueToday:
    """Tests for get_tasks_due_today() method (Phase-2 US5)."""

    def test_get_tasks_due_today_returns_today_tasks(self, empty_manager):
        """Test get_tasks_due_today() returns tasks due today."""
        today = datetime.now()
        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)

        due_today = empty_manager.add_task("Due today", due_date=today)

        # Create task with future date, then manually set to yesterday for testing
        due_yesterday = empty_manager.add_task("Due yesterday", due_date=tomorrow)
        due_yesterday.due_date = yesterday

        empty_manager.add_task("Due tomorrow", due_date=tomorrow)

        result = empty_manager.get_tasks_due_today()

        assert len(result) == 1
        assert result[0].id == due_today.id


class TestGetUpcomingTasks:
    """Tests for get_upcoming_tasks() method (Phase-2 US5)."""

    def test_get_upcoming_tasks_returns_next_7_days(self, empty_manager):
        """Test get_upcoming_tasks() returns tasks due in next 7 days."""
        day_3 = datetime.now() + timedelta(days=3)
        day_10 = datetime.now() + timedelta(days=10)

        upcoming = empty_manager.add_task("Upcoming task", due_date=day_3)
        empty_manager.add_task("Far future task", due_date=day_10)

        result = empty_manager.get_upcoming_tasks()

        assert len(result) == 1
        assert result[0].id == upcoming.id

    def test_get_upcoming_tasks_excludes_today_and_overdue(self, empty_manager):
        """Test get_upcoming_tasks() excludes today and overdue tasks."""
        today = datetime.now()
        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)

        empty_manager.add_task("Due today", due_date=today)

        # Create task with future date, then manually set to yesterday for testing
        overdue_task = empty_manager.add_task("Overdue", due_date=tomorrow)
        overdue_task.due_date = yesterday

        upcoming = empty_manager.add_task("Tomorrow", due_date=tomorrow)

        result = empty_manager.get_upcoming_tasks()

        assert len(result) == 1
        assert result[0].id == upcoming.id


# Phase-2 Tests: US6 - Recurring Tasks

class TestAddTaskWithRecurrence:
    """Tests for add_task() with recurrence_rule parameter (Phase-2 US6)."""

    def test_add_task_with_recurrence_rule_daily(self, empty_manager):
        """Test add_task() with valid daily recurrence_rule."""
        future_date = datetime.now() + timedelta(days=1)
        task = empty_manager.add_task(
            "Daily task",
            due_date=future_date,
            recurrence_rule="daily"
        )

        assert task.recurrence_rule == "daily"
        assert task.due_date == future_date

    def test_add_task_with_recurrence_rule_weekly(self, empty_manager):
        """Test add_task() with valid weekly recurrence_rule."""
        future_date = datetime.now() + timedelta(days=1)
        task = empty_manager.add_task(
            "Weekly task",
            due_date=future_date,
            recurrence_rule="weekly"
        )

        assert task.recurrence_rule == "weekly"

    def test_add_task_with_recurrence_rule_monthly(self, empty_manager):
        """Test add_task() with valid monthly recurrence_rule."""
        future_date = datetime.now() + timedelta(days=1)
        task = empty_manager.add_task(
            "Monthly task",
            due_date=future_date,
            recurrence_rule="monthly"
        )

        assert task.recurrence_rule == "monthly"

    def test_add_task_without_recurrence_defaults_to_none(self, empty_manager):
        """Test add_task() defaults to None when recurrence_rule not specified."""
        task = empty_manager.add_task("Non-recurring task")

        assert task.recurrence_rule is None
