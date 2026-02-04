"""Integration tests for task creation conversation flow."""
import pytest
from httpx import AsyncClient

# These tests will FAIL initially (Red phase of TDD)
# Implementation will make them pass in subsequent tasks


@pytest.mark.asyncio
async def test_create_conversation_and_add_task(client: AsyncClient, auth_headers_user_a: dict):
    """Test full flow: create conversation and add task via chat."""
    auth_headers = auth_headers_user_a
    # Step 1: Create a new conversation
    response = await client.post(
        "/api/v1/conversations",
        json={"title": "Test conversation"},
        headers=auth_headers
    )
    assert response.status_code == 201
    conversation = response.json()
    conversation_id = conversation["id"]

    # Step 2: Send message to add a task
    response = await client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "Add a task to buy groceries"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "user_message" in data
    assert "assistant_message" in data
    assert data["user_message"]["content"] == "Add a task to buy groceries"
    assert "groceries" in data["assistant_message"]["content"].lower()

    # Verify tool was executed
    assert "tool_executions" in data
    assert len(data["tool_executions"]) > 0
    assert data["tool_executions"][0]["tool_name"] == "add_task"
    assert data["tool_executions"][0]["status"] == "success"


@pytest.mark.asyncio
async def test_add_task_with_initial_message(client: AsyncClient, auth_headers_user_a: dict):
    """Test creating conversation with initial message to add task."""
    auth_headers = auth_headers_user_a
    response = await client.post(
        "/api/v1/conversations",
        json={
            "title": "Quick task",
            "initial_message": "remind me to call John tomorrow at 2pm"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()

    # Verify conversation created with messages
    assert "id" in data
    assert "messages" in data
    assert len(data["messages"]) >= 2  # User message + assistant response

    # Verify task was created
    user_msg = next(m for m in data["messages"] if m["role"] == "user")
    assert "call John" in user_msg["content"]

    assistant_msg = next(m for m in data["messages"] if m["role"] == "assistant")
    assert "call John" in assistant_msg["content"].lower()


@pytest.mark.asyncio
async def test_add_task_natural_language_parsing(client: AsyncClient, auth_headers_user_a: dict):
    """Test that agent correctly parses natural language task details."""
    auth_headers = auth_headers_user_a
    # Create conversation
    response = await client.post(
        "/api/v1/conversations",
        json={"title": "NL test"},
        headers=auth_headers
    )
    conversation_id = response.json()["id"]

    # Send message with embedded task details
    response = await client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "high priority: finish report by Friday"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()

    # Verify tool was called with correct parameters
    tool_exec = data["tool_executions"][0]
    params = tool_exec["parameters"]
    assert "finish report" in params["title"]
    assert params["priority"] == "high"
    assert "due_date" in params  # Should parse "Friday"


@pytest.mark.asyncio
async def test_conversation_not_found(client: AsyncClient, auth_headers_user_a: dict):
    """Test sending message to non-existent conversation."""
    auth_headers = auth_headers_user_a
    response = await client.post(
        "/api/v1/conversations/99999/messages",
        json={"content": "test message"},
        headers=auth_headers
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_rate_limiting(client: AsyncClient, auth_headers_user_a: dict):
    """Test that rate limiting is enforced (10 requests/minute)."""
    auth_headers = auth_headers_user_a
    # Create conversation
    response = await client.post(
        "/api/v1/conversations",
        json={"title": "Rate limit test"},
        headers=auth_headers
    )
    conversation_id = response.json()["id"]

    # Send 11 messages rapidly (should hit rate limit on 11th)
    for i in range(11):
        response = await client.post(
            f"/api/v1/conversations/{conversation_id}/messages",
            json={"content": f"test message {i}"},
            headers=auth_headers
        )
        if i < 10:
            assert response.status_code == 200
        else:
            assert response.status_code == 429  # Too Many Requests
