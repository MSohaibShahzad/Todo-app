# Quickstart: Conversational AI Integration

**Feature**: 004-conversational-ai
**Date**: 2026-01-15
**Target Audience**: Developers implementing the conversational AI feature

## Overview

This quickstart guide walks through implementing conversational AI task management in the Todo app. By the end, users will be able to manage tasks through natural language conversation.

**Time Estimate**: 1-2 weeks for full implementation

## Prerequisites

- Phase 2 full-stack app running (Next.js frontend + FastAPI backend)
- PostgreSQL database (Neon) with existing task tables
- Better-Auth authentication working
- Node.js 18+ and Python 3.11+ installed
- OpenAI API key (GPT-4 Turbo access)
- **Context7 MCP server** configured for accessing up-to-date library documentation

## Architecture Overview

```
┌─────────────────┐
│  Next.js App    │
│  (ChatKit UI)   │
└────────┬────────┘
         │ HTTP/SSE
         ↓
┌─────────────────┐
│  FastAPI        │
│  /chat endpoint │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌────────┐  ┌──────────────────┐
│   DB   │  │ OpenAI Agents SDK│
│ (State)│  │     (Agent)      │
└────────┘  └──────┬───────────┘
                   │
            ┌──────┴──────┐
            │ MCP Server  │
            │   (Tools)   │
            └─────────────┘
```

## Implementation Steps

### Step 1: Set Up Database Schema (30 minutes)

**Goal**: Add conversation and message tables to store chat history.

1. **Create migration file**:
```bash
cd backend
alembic revision -m "add_conversations_and_messages"
```

2. **Edit migration** (`backend/alembic/versions/002_add_conversations.py`):
   - Copy schema from `/specs/004-conversational-ai/data-model.md`
   - Add `conversations`, `messages`, and `tool_executions` tables
   - Create indexes for user_id, updated_at, conversation_id

3. **Run migration**:
```bash
alembic upgrade head
```

4. **Verify tables**:
```bash
psql $DATABASE_URL -c "\dt"
# Should show: conversations, messages, tool_executions
```

**Acceptance**: Tables exist with correct columns and indexes.

---

### Step 2: Create SQLModel Models (30 minutes)

**Goal**: Define Python models for conversations and messages.

1. **Create model files**:
```bash
touch backend/src/models/conversation.py
touch backend/src/models/message.py
```

2. **Implement models** (reference: `/specs/004-conversational-ai/data-model.md`):
   - `Conversation` model with relationships
   - `Message` model with MessageRole enum
   - `ToolExecution` model with ToolExecutionStatus enum

3. **Update `__init__.py`**:
```python
# backend/src/models/__init__.py
from .conversation import Conversation, Message, ToolExecution, MessageRole, ToolExecutionStatus
```

4. **Test models**:
```python
# Manual test in Python REPL
from src.models import Conversation, Message
conv = Conversation(user_id="test_user", title="Test")
msg = Message(conversation_id=1, role="user", content="Hello")
print(conv, msg)
```

**Acceptance**: Models defined and importable without errors.

---

### Step 3: Build MCP Server (2-3 hours)

**Goal**: Expose task operations as MCP tools for AI agents.

**Important**: Use **Context7 MCP server** to access the latest MCP SDK documentation and best practices during implementation.

1. **Install MCP SDK**:
```bash
cd backend
pip install mcp
```

2. **Query Context7 for MCP implementation guidance**:
   - Use Context7 MCP server to get up-to-date documentation on MCP tool definitions
   - Query for Python SDK examples: "How to create MCP tools in Python"
   - Reference: Model Context Protocol Python SDK best practices

3. **Create MCP server file**:
```bash
mkdir -p backend/src/mcp
touch backend/src/mcp/todo_server.py
```

3. **Implement tools** (reference: `/specs/004-conversational-ai/contracts/mcp-tools.yaml`):
```python
from mcp.server import Server
from mcp.types import TextContent
from src.services.task_service import TaskService

server = Server("todo-mcp-server")

@server.tool()
async def add_task(
    user_id: str,
    title: str,
    description: str = None,
    priority: str = "medium",
    category: str = None,
    due_date: str = None
) -> TextContent:
    """Add a new task."""
    # Implementation using TaskService
    task = await TaskService.create_task(user_id, title, ...)
    return TextContent(
        type="text",
        text=f"Task created: {task.id} - {task.title}"
    )

# Implement remaining tools: list_tasks, update_task, delete_task,
# mark_task_complete, search_tasks, bulk_delete_tasks
```

4. **Add entry point**:
```python
# backend/src/mcp/__main__.py
from .todo_server import server

if __name__ == "__main__":
    server.run()
```

5. **Test MCP server**:
```bash
python -m src.mcp
# Should start without errors
```

**Acceptance**: MCP server runs and exposes all 7 tools.

---

### Step 4: Integrate OpenAI Agents SDK (2 hours)

**Goal**: Set up AI agent to interpret user intent and call MCP tools.

**Important**: Use **Context7** to access latest OpenAI Agents SDK documentation and agent patterns.

1. **Install dependencies**:
```bash
cd backend
pip install openai
```

2. **Query Context7 for Agents SDK guidance**:
   - Query: "OpenAI Agents SDK setup and tool integration"
   - Get examples of stateless agent implementations
   - Learn best practices for function calling with Agents SDK

3. **Create agent service**:
```bash
touch backend/src/services/ai_agent_service.py
```

3. **Implement agent** (reference: `/specs/004-conversational-ai/research.md`):
```python
from openai import OpenAI
from src.mcp.todo_server import (
    add_task, list_tasks, update_task, delete_task,
    mark_task_complete, search_tasks, bulk_delete_tasks
)

client = OpenAI()

task_agent = {
    "name": "Task Manager",
    "instructions": """
    You are a helpful task management assistant.
    Help users manage their todo tasks through natural conversation.
    Use the provided tools to perform operations.
    Always confirm actions with clear, friendly responses.
    """,
    "tools": [
        add_task, list_tasks, update_task, delete_task,
        mark_task_complete, search_tasks, bulk_delete_tasks
    ]
}

async def process_message(
    user_id: str,
    message: str,
    conversation_history: list
) -> dict:
    """Process user message and return agent response."""
    # Add user message to history
    messages = conversation_history + [
        {"role": "user", "content": message}
    ]

    # Run agent
    response = await client.agents.run(
        agent=task_agent,
        messages=messages,
        context_variables={"user_id": user_id}
    )

    return {
        "message": response.messages[-1]["content"],
        "tool_calls": response.tool_calls
    }
```

4. **Test agent** (in Python REPL):
```python
from src.services.ai_agent_service import process_message

result = await process_message(
    user_id="test_user",
    message="Add a task to buy groceries",
    conversation_history=[]
)
print(result)
# Should return: {"message": "I've added...", "tool_calls": [...]}
```

**Acceptance**: Agent successfully interprets intent and calls appropriate tools.

---

### Step 5: Create Chat API Endpoints (2 hours)

**Goal**: Expose stateless chat API for frontend to consume.

1. **Create chat router**:
```bash
touch backend/src/api/chat.py
```

2. **Implement endpoints** (reference: `/specs/004-conversational-ai/contracts/chat-api.yaml`):
```python
from fastapi import APIRouter, Depends, HTTPException
from src.auth.dependencies import get_current_user
from src.services.ai_agent_service import process_message
from src.models import Conversation, Message, User
from src.database import get_session

router = APIRouter(prefix="/conversations", tags=["chat"])

@router.post("")
async def create_conversation(
    title: str = None,
    initial_message: str = None,
    user: User = Depends(get_current_user),
    session = Depends(get_session)
):
    """Create new conversation."""
    # Check active conversation limit (max 3)
    # Create conversation record
    # If initial_message, process it
    pass

@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    user: User = Depends(get_current_user),
    session = Depends(get_session)
):
    """Get conversation with message history."""
    # Verify ownership
    # Load conversation + last 20 messages
    pass

@router.post("/{conversation_id}/messages")
async def send_message(
    conversation_id: int,
    content: str,
    user: User = Depends(get_current_user),
    session = Depends(get_session)
):
    """Send message and receive AI response."""
    # 1. Verify conversation ownership
    # 2. Load conversation history
    # 3. Process message with AI agent
    # 4. Persist user + assistant messages
    # 5. Log tool executions
    # 6. Return response
    pass

@router.post("/{conversation_id}/undo")
async def undo_last_action(
    conversation_id: int,
    user: User = Depends(get_current_user),
    session = Depends(get_session)
):
    """Undo last tool execution."""
    # Find last successful tool execution
    # Call inverse tool (e.g., delete_task for add_task)
    pass
```

3. **Register router**:
```python
# backend/src/api/__init__.py
from .chat import router as chat_router

api_router.include_router(chat_router)
```

4. **Test endpoints**:
```bash
curl -X POST http://localhost:8000/api/v1/conversations \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "initial_message": "Show my tasks"}'
```

**Acceptance**: All chat endpoints work and return proper responses.

---

### Step 6: Add Rate Limiting (1 hour)

**Goal**: Prevent API abuse with per-user rate limits.

1. **Install dependencies**:
```bash
pip install redis slowapi
```

2. **Configure Redis** (update `.env`):
```env
REDIS_URL=redis://localhost:6379
```

3. **Add rate limiter**:
```python
# backend/src/middleware/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Apply to chat endpoints
@router.post("/{conversation_id}/messages")
@limiter.limit("10/minute")
async def send_message(...):
    pass
```

**Acceptance**: Rate limiting enforced; returns 429 after exceeding limits.

---

### Step 7: Frontend Chat UI (2-3 hours)

**Goal**: Add conversational interface using OpenAI ChatKit.

**Important**: Use **Context7** for React and Next.js 14 App Router best practices.

1. **Install ChatKit**:
```bash
cd frontend
npm install @openai/chatkit
```

2. **Query Context7 for guidance**:
   - Query: "OpenAI ChatKit React integration examples"
   - Query: "Next.js 14 App Router client component patterns"
   - Get best practices for real-time chat UI

3. **Create conversation page**:
```bash
mkdir -p app/chat
touch app/chat/page.tsx
```

3. **Implement UI**:
```tsx
// app/chat/page.tsx
'use client'

import { useState, useEffect } from 'react'
import { ChatContainer, MessageList, MessageInput } from '@openai/chatkit'
import { api } from '@/lib/api'

export default function ChatPage() {
  const [conversations, setConversations] = useState([])
  const [activeConversation, setActiveConversation] = useState(null)
  const [messages, setMessages] = useState([])

  const handleSendMessage = async (content: string) => {
    // Send to backend
    const response = await api.sendMessage(activeConversation.id, content)

    // Update messages
    setMessages([
      ...messages,
      response.user_message,
      response.assistant_message
    ])
  }

  return (
    <div className="flex h-screen">
      {/* Conversation list sidebar */}
      <aside className="w-64 border-r">
        {/* List conversations */}
      </aside>

      {/* Chat area */}
      <main className="flex-1">
        <ChatContainer>
          <MessageList messages={messages} />
          <MessageInput onSend={handleSendMessage} />
        </ChatContainer>
      </main>
    </div>
  )
}
```

4. **Add API client methods**:
```typescript
// lib/api.ts
export const api = {
  // ... existing methods

  async createConversation(title?: string, initialMessage?: string) {
    return await fetch('/api/v1/conversations', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${getToken()}` },
      body: JSON.stringify({ title, initial_message: initialMessage })
    }).then(r => r.json())
  },

  async getConversations() {
    return await fetch('/api/v1/conversations', {
      headers: { 'Authorization': `Bearer ${getToken()}` }
    }).then(r => r.json())
  },

  async sendMessage(conversationId: number, content: string) {
    return await fetch(`/api/v1/conversations/${conversationId}/messages`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${getToken()}` },
      body: JSON.stringify({ content })
    }).then(r => r.json())
  }
}
```

5. **Add navigation**:
```tsx
// Update main navigation to include "Chat" link
<Link href="/chat">Chat with AI</Link>
```

**Acceptance**: Users can create conversations, send messages, and receive AI responses.

---

### Step 8: Implement Undo Functionality (1 hour)

**Goal**: Allow users to reverse last AI action.

1. **Backend undo logic**:
```python
# backend/src/services/undo_service.py
async def undo_last_tool_execution(conversation_id: int, user_id: str):
    """Reverse last successful tool execution."""
    # Get last tool execution
    last_exec = await get_last_tool_execution(conversation_id)

    if not last_exec:
        raise ValueError("No recent action to undo")

    # Call inverse tool
    if last_exec.tool_name == "add_task":
        task_id = last_exec.result["task_id"]
        await delete_task(user_id, task_id)
        return f"Undone: Task {task_id} deleted"

    elif last_exec.tool_name == "delete_task":
        # Restore deleted task from execution parameters
        pass

    # ... handle other tools
```

2. **Frontend undo button**:
```tsx
<button onClick={() => handleUndo()}>
  Undo Last Action
</button>
```

**Acceptance**: Users can undo last action (task creation, deletion, etc.).

---

### Step 9: Add Conversation Retention Policy (1 hour)

**Goal**: Auto-delete conversations older than 30 days.

1. **Create cleanup service**:
```python
# backend/src/services/cleanup_service.py
from datetime import datetime, timedelta

async def cleanup_old_conversations():
    """Delete conversations older than 30 days."""
    cutoff = datetime.utcnow() - timedelta(days=30)
    # Delete conversations with updated_at < cutoff
    # Cascading deletes handle messages and tool_executions
```

2. **Schedule cleanup job** (using APScheduler):
```python
# backend/src/main.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.add_job(
    cleanup_old_conversations,
    'cron',
    hour=2,  # 2 AM daily
    minute=0
)
scheduler.start()
```

**Acceptance**: Old conversations automatically deleted daily.

---

### Step 10: Testing & Refinement (2-3 hours)

**Goal**: Ensure reliability and accuracy.

1. **Unit tests**:
```python
# tests/unit/test_ai_agent.py
async def test_add_task_intent():
    result = await process_message(
        user_id="test",
        message="Add a task to buy milk",
        conversation_history=[]
    )
    assert "add_task" in result["tool_calls"][0]["tool_name"]
    assert "milk" in result["tool_calls"][0]["parameters"]["title"]
```

2. **Integration tests**:
```python
# tests/integration/test_chat_flow.py
async def test_full_conversation():
    # Create conversation
    # Send message "show my tasks"
    # Verify tool called and response returned
    # Send message "add task: test"
    # Verify task created
    # Send "undo"
    # Verify task deleted
```

3. **Load testing** (optional):
```bash
locust -f tests/load/chat_load_test.py --host http://localhost:8000
```

**Acceptance**: All tests pass; system handles concurrent conversations.

---

## Environment Variables

Add to `.env` files:

**Backend** (`backend/.env`):
```env
OPENAI_API_KEY=sk-...
REDIS_URL=redis://localhost:6379
AI_MODEL=gpt-4-turbo
RATE_LIMIT_REQUESTS_PER_MINUTE=10
CONVERSATION_RETENTION_DAYS=30
MAX_ACTIVE_CONVERSATIONS_PER_USER=3
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running the System

**Start all services**:
```bash
# Terminal 1: Backend
cd backend
uvicorn src.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Redis (if not running as service)
redis-server
```

**Access**:
- Frontend: http://localhost:3000
- Chat UI: http://localhost:3000/chat
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Common Issues & Solutions

### Issue: "OpenAI API rate limit exceeded"
**Solution**: Reduce requests or upgrade OpenAI plan tier.

### Issue: "Conversation limit reached (3 active)"
**Solution**: Archive old conversations or increase limit in config.

### Issue: "AI misinterprets user intent"
**Solution**: Improve agent instructions or add more examples in prompt.

### Issue: "Tool execution fails silently"
**Solution**: Check tool_executions table for error_message; improve error handling.

### Issue: "Conversation history too long (token limit)"
**Solution**: Truncate to last 20 messages in context loading.

## Next Steps

After completing this quickstart:

1. **Monitor Usage**: Track OpenAI API costs and user adoption
2. **Improve Accuracy**: Collect user feedback and refine agent instructions
3. **Add Features**: Streaming responses, conversation search, analytics
4. **Optimize Performance**: Cache frequently accessed data, reduce latency
5. **Scale**: Add load balancer, multiple backend instances

## Resources

- **Research Doc**: `/specs/004-conversational-ai/research.md`
- **Data Model**: `/specs/004-conversational-ai/data-model.md`
- **API Contract**: `/specs/004-conversational-ai/contracts/chat-api.yaml`
- **MCP Tools**: `/specs/004-conversational-ai/contracts/mcp-tools.yaml`
- **Context7 MCP Server**: Use for up-to-date library documentation during implementation
- **OpenAI Agents SDK**: https://platform.openai.com/docs/agents
- **MCP SDK**: https://github.com/modelcontextprotocol/python-sdk
- **ChatKit**: https://github.com/openai/chatkit

### Using Context7 During Implementation

Throughout the implementation process, leverage the **Context7 MCP server** to access the latest documentation:

**Key Queries**:
- "MCP Python SDK tool definition examples"
- "OpenAI Agents SDK stateless agent patterns"
- "FastAPI async endpoint best practices"
- "Next.js 14 App Router server vs client components"
- "OpenAI ChatKit message rendering examples"
- "Redis rate limiting patterns in Python"
- "SQLModel relationship definitions"

**Benefits**:
- Get current API documentation (not outdated tutorials)
- Access real code examples from official SDKs
- Learn best practices directly from library maintainers
- Avoid deprecated patterns and methods

## Success Criteria

✅ Users can create conversations and send messages
✅ AI correctly interprets task management intents (90% accuracy)
✅ All task operations work through conversation
✅ Undo functionality works for last action
✅ Rate limiting prevents abuse
✅ Old conversations auto-deleted after 30 days
✅ System handles 100 concurrent conversations
✅ Average response time < 2 seconds
✅ Existing UI functionality unaffected
