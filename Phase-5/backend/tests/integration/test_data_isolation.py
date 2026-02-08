"""Test data isolation between users.

Verifies that users can only access their own tasks and cannot
access or modify other users' tasks.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task
from src.models.user import User


class TestDataIsolation:
    """Test suite for data isolation security."""

    @pytest.mark.asyncio
    async def test_user_can_only_see_own_tasks(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        user_a: User,
        user_b: User,
        task_user_a: Task,
        task_user_b: Task,
        auth_headers_user_a: dict,
    ):
        """T085: Verify user A cannot see user B's tasks in task list.

        Test: GET /api/v1/tasks should only return tasks belonging to authenticated user.
        """
        # User A requests their task list
        response = await client.get("/api/v1/tasks", headers=auth_headers_user_a)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        tasks = response.json()
        assert isinstance(tasks, list), "Response should be a list"
        assert len(tasks) == 1, f"User A should see only 1 task, got {len(tasks)}"

        # Verify only User A's task is returned
        task = tasks[0]
        assert task["id"] == task_user_a.id, "Task ID should match User A's task"
        assert task["title"] == task_user_a.title
        assert task["user_id"] == user_a.id

        # Verify User B's task is NOT in the list
        task_ids = [t["id"] for t in tasks]
        assert task_user_b.id not in task_ids, "User B's task should not be visible to User A"

    @pytest.mark.asyncio
    async def test_user_cannot_access_other_users_task(
        self,
        client: AsyncClient,
        user_a: User,
        user_b: User,
        task_user_b: Task,
        auth_headers_user_a: dict,
    ):
        """T086: Verify 404 error when user A tries to access user B's task by ID.

        Test: GET /api/v1/tasks/{task_id} should return 404 when accessing other user's task.
        """
        # User A tries to access User B's task directly by ID
        response = await client.get(
            f"/api/v1/tasks/{task_user_b.id}",
            headers=auth_headers_user_a
        )

        # Should return 404 (not 403) to avoid leaking task ID existence
        assert response.status_code == 404, (
            f"Expected 404 when accessing other user's task, got {response.status_code}"
        )

        error_data = response.json()
        assert "detail" in error_data, "Error response should contain 'detail' field"
        assert "not found" in error_data["detail"].lower(), (
            "Error message should indicate task not found"
        )

    @pytest.mark.asyncio
    async def test_user_cannot_update_other_users_task(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        user_a: User,
        user_b: User,
        task_user_b: Task,
        auth_headers_user_a: dict,
        auth_headers_user_b: dict,
    ):
        """T086: Verify user A cannot update user B's task.

        Test: PUT /api/v1/tasks/{task_id} should return 404 when updating other user's task.
        """
        original_title = task_user_b.title
        original_completed = task_user_b.completed

        update_data = {
            "title": "Hacked Title",
            "description": "User A trying to modify User B's task",
            "completed": True,
        }

        # User A tries to update User B's task
        response = await client.put(
            f"/api/v1/tasks/{task_user_b.id}",
            json=update_data,
            headers=auth_headers_user_a
        )

        assert response.status_code == 404, (
            f"Expected 404 when updating other user's task, got {response.status_code}"
        )

        # Verify task was NOT modified by having User B fetch it
        response_b = await client.get(
            f"/api/v1/tasks/{task_user_b.id}",
            headers=auth_headers_user_b
        )
        assert response_b.status_code == 200
        task_data = response_b.json()
        assert task_data["title"] == original_title, "Title should not be changed"
        assert task_data["completed"] == original_completed, "Status should not be changed"

    @pytest.mark.asyncio
    async def test_user_cannot_delete_other_users_task(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        user_a: User,
        user_b: User,
        task_user_b: Task,
        auth_headers_user_a: dict,
    ):
        """T087: Verify DELETE returns 404 for other user's task.

        Test: DELETE /api/v1/tasks/{task_id} should return 404 and not delete other user's task.
        """
        # User A tries to delete User B's task
        response = await client.delete(
            f"/api/v1/tasks/{task_user_b.id}",
            headers=auth_headers_user_a
        )

        assert response.status_code == 404, (
            f"Expected 404 when deleting other user's task, got {response.status_code}"
        )

        # Verify task still exists in database
        from sqlalchemy import select
        result = await db_session.execute(
            select(Task).where(Task.id == task_user_b.id)
        )
        task_in_db = result.scalar_one_or_none()

        assert task_in_db is not None, "User B's task should still exist after failed delete"
        assert task_in_db.id == task_user_b.id
        assert task_in_db.user_id == user_b.id

    @pytest.mark.asyncio
    async def test_user_cannot_complete_other_users_task(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        user_a: User,
        user_b: User,
        task_user_b: Task,
        auth_headers_user_a: dict,
        auth_headers_user_b: dict,
    ):
        """Verify user A cannot toggle completion status of user B's task.

        Test: PATCH /api/v1/tasks/{task_id}/complete should return 404.
        """
        original_completed = task_user_b.completed

        # User A tries to mark User B's task as complete
        # Note: completed is a query parameter, not in request body
        response = await client.patch(
            f"/api/v1/tasks/{task_user_b.id}/complete?completed=true",
            headers=auth_headers_user_a
        )

        assert response.status_code == 404, (
            f"Expected 404 when toggling other user's task, got {response.status_code}"
        )

        # Verify task completion status unchanged by having User B fetch it
        response_b = await client.get(
            f"/api/v1/tasks/{task_user_b.id}",
            headers=auth_headers_user_b
        )
        assert response_b.status_code == 200
        task_data = response_b.json()
        assert task_data["completed"] == original_completed, (
            "Completion status should not be changed"
        )

    @pytest.mark.asyncio
    async def test_unauthenticated_request_rejected(
        self,
        client: AsyncClient,
        task_user_a: Task,
    ):
        """Verify unauthenticated requests are rejected with 401.

        Test: Requests without Authorization header should return 401.
        """
        # Try to access tasks without authentication
        response = await client.get("/api/v1/tasks")
        assert response.status_code == 401, "Unauthenticated GET should return 401"

        # Try to create task without authentication
        response = await client.post(
            "/api/v1/tasks",
            json={"title": "Unauthorized Task"}
        )
        assert response.status_code == 401, "Unauthenticated POST should return 401"

        # Try to access specific task without authentication
        response = await client.get(f"/api/v1/tasks/{task_user_a.id}")
        assert response.status_code == 401, "Unauthenticated GET by ID should return 401"

        # Try to delete task without authentication
        response = await client.delete(f"/api/v1/tasks/{task_user_a.id}")
        assert response.status_code == 401, "Unauthenticated DELETE should return 401"
