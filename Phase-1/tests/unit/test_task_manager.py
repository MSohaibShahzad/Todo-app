"""Unit tests for TaskManager service."""

import pytest
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
