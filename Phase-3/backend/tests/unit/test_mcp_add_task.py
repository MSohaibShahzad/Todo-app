"""Unit tests for add_task MCP tool."""
import pytest
from datetime import datetime
from unittest.mock import patch, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User

# These tests will FAIL initially (Red phase of TDD)
# Implementation will make them pass in subsequent tasks


@pytest.mark.asyncio
async def test_add_task_basic(db_session: AsyncSession, user_a: User):
    """Test adding a basic task with only title."""
    from src.mcp.todo_server import add_task

    # Mock get_db_session to return our test session
    with patch('src.mcp.todo_server.get_db_session') as mock_get_db:
        # Create an async context manager that yields the test session
        async def mock_context():
            yield db_session

        mock_get_db.return_value.__aenter__ = AsyncMock(return_value=db_session)
        mock_get_db.return_value.__aexit__ = AsyncMock(return_value=None)

        result = await add_task(
            user_id=user_a.id,
            title="Buy groceries"
        )

        assert result is not None
        assert "Buy groceries" in result.text
        assert "created" in result.text.lower()


@pytest.mark.asyncio
async def test_add_task_with_all_fields(db_session: AsyncSession, user_a: User):
    """Test adding a task with all optional fields."""
    from src.mcp.todo_server import add_task

    # Mock get_db_session to return our test session
    with patch('src.mcp.todo_server.get_db_session') as mock_get_db:
        mock_get_db.return_value.__aenter__ = AsyncMock(return_value=db_session)
        mock_get_db.return_value.__aexit__ = AsyncMock(return_value=None)

        result = await add_task(
            user_id=user_a.id,
            title="Call John",
            description="Discuss project timeline",
            priority="high",
            category="work",
            due_date="2026-01-16T14:00:00Z"
        )

        assert result is not None
        assert "Call John" in result.text
        assert "created" in result.text.lower()


@pytest.mark.asyncio
async def test_add_task_validation_empty_title():
    """Test that empty title is rejected."""
    from src.mcp.todo_server import add_task

    with pytest.raises(ValueError, match="title"):
        await add_task(
            user_id="test_user_123",
            title=""
        )


@pytest.mark.asyncio
async def test_add_task_validation_invalid_priority():
    """Test that invalid priority is rejected."""
    from src.mcp.todo_server import add_task

    with pytest.raises(ValueError, match="priority"):
        await add_task(
            user_id="test_user_123",
            title="Test task",
            priority="invalid_priority"
        )


@pytest.mark.asyncio
async def test_add_task_validation_invalid_date():
    """Test that invalid date format is rejected."""
    from src.mcp.todo_server import add_task

    with pytest.raises(ValueError, match="date"):
        await add_task(
            user_id="test_user_123",
            title="Test task",
            due_date="not-a-date"
        )
