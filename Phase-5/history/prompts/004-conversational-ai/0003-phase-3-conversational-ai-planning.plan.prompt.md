---
id: 0003
title: Phase 3 Conversational AI Planning
stage: plan
date: 2026-01-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: 004-conversational-ai
branch: 004-conversational-ai
user: sohaib
command: /sp.plan
labels: ["planning", "conversational-ai", "architecture", "mcp", "openai-swarm"]
links:
  spec: /specs/004-conversational-ai/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-conversational-ai/plan.md
  - specs/004-conversational-ai/research.md
  - specs/004-conversational-ai/data-model.md
  - specs/004-conversational-ai/quickstart.md
  - specs/004-conversational-ai/contracts/chat-api.yaml
  - specs/004-conversational-ai/contracts/mcp-tools.yaml
tests:
  - None (planning phase - no tests yet)
---

## Prompt

Title: Phase III – Conversational AI Integration Plan

Plan the implementation of a conversational interface that allows users
to manage all Todo features via natural language.

System Layers:
- Frontend (Chat UI)
- Backend API (chat endpoint)
- AI Agent layer
- MCP Server (tools)
- Database (tasks + conversation state)

AI Agent Layer:
- Use OpenAI Agents SDK for conversational logic
- Agents interpret user intent and decide which tool to call
- Agents are stateless and do not store or mutate data directly

MCP Server:
- Build an MCP server using the Official MCP SDK
- Expose one tool per task operation, including:
  - add_task
  - list_tasks
  - update_task
  - delete_task
  - mark_task_complete
- MCP tools must be stateless
- All reads/writes occur through the database

Chat Endpoint:
- Provide a stateless chat API endpoint
- On each request:
  - Load conversation context from the database
  - Forward user input and context to the AI agent
  - Execute selected MCP tools
  - Persist updated conversation state back to the database

State Management:
- No in-memory session state
- Conversation history stored in database
- Task data stored in database
- State reconstructed per request

Frontend:
- Use OpenAI ChatKit for the chat interface
- Send user messages to backend chat endpoint
- Render conversational responses and task feedback

Integration Rules:
- Agents cannot access the database directly
- All task mutations must go through MCP tools
- MCP server remains independent from UI and agent logic
- Existing backend and database are reused

Outcome:
- Users manage tasks entirely via conversation
- System remains stateless, modular, and scalable

User also mentioned: "also mention that use context7 mcp server for implementation"

## Response snapshot

Successfully completed Phase 0 (Research) and Phase 1 (Design) for conversational AI integration:

**Phase 0 - Research (research.md)**:
- Selected OpenAI Swarm for lightweight, stateless agent orchestration
- Chose MCP Python SDK for standardized tool interface
- Selected OpenAI ChatKit for frontend chat UI components
- Designed PostgreSQL schema for conversation state (3 new tables)
- Decided on Redis token bucket for per-user rate limiting
- GPT-4 Turbo for AI model (cost/quality balance)
- Documented integration architecture and stateless request flow

**Phase 1 - Design Artifacts**:

1. **data-model.md**: Complete database schema
   - Conversation model (user sessions)
   - Message model (chat history)
   - ToolExecution model (audit trail)
   - Validation rules and query patterns
   - Migration script for Alembic

2. **contracts/chat-api.yaml**: OpenAPI specification
   - POST /conversations (create)
   - GET /conversations/{id} (retrieve with history)
   - POST /conversations/{id}/messages (send message, get AI response)
   - POST /conversations/{id}/undo (reverse last action)
   - POST /conversations/{id}/stream (streaming responses)

3. **contracts/mcp-tools.yaml**: MCP tool definitions
   - 7 tools: add_task, list_tasks, update_task, delete_task, mark_task_complete, search_tasks, bulk_delete_tasks
   - Structured parameters and return schemas
   - Error codes and examples

4. **quickstart.md**: 10-step implementation guide
   - Database setup → Models → MCP Server → AI Agent → Chat API → Rate Limiting → Frontend UI → Undo → Retention → Testing
   - Includes Context7 MCP server usage notes for accessing up-to-date documentation
   - Time estimates and acceptance criteria per step

5. **plan.md**: Complete architectural plan
   - Technical context (Python 3.11, FastAPI, Next.js 14, PostgreSQL, Redis)
   - Constitution compliance check (all gates passing)
   - Project structure (backend/frontend file layout)
   - Complexity tracking (justified all additions)
   - 7 architecture decisions with rationale and trade-offs
   - Risk assessment with mitigation strategies
   - Success criteria mapped to implementation approach
   - 4-phase deployment strategy

**Key Architecture Decisions**:
1. OpenAI Swarm for agents (stateless, lightweight)
2. MCP for tool layer (standardized, constitution-compliant)
3. PostgreSQL for state (ACID, existing infrastructure)
4. OpenAI ChatKit for UI (pre-built components)
5. Redis for rate limiting (distributed, burst-friendly)
6. 30-day auto-delete for retention (storage + privacy)
7. Inverse tool execution for undo (trust + safety)

**Constitution Compliance**: All requirements satisfied
- Stateless agents and endpoints ✓
- Database-backed state ✓
- MCP architecture ✓
- No breaking changes ✓
- Clean separation of concerns ✓

**Context7 Integration**: Documented throughout quickstart.md
- Use Context7 MCP server for accessing latest documentation during implementation
- Specific queries listed for MCP SDK, OpenAI Swarm, FastAPI, Next.js, ChatKit
- Benefits: current docs, official examples, best practices

**Next Steps**: Ready for `/sp.tasks` to generate implementation task breakdown

## Outcome

- ✅ Impact: Complete architectural plan for Phase 3 conversational AI feature with all design artifacts generated
- 🧪 Tests: None (planning phase - tests will be defined in tasks.md)
- 📁 Files: 6 new specification files (plan.md, research.md, data-model.md, quickstart.md, 2 contract files)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation task breakdown
- 🧠 Reflection: Successfully planned complex multi-layer architecture (frontend, backend, AI agent, MCP server, database) while maintaining stateless design and constitution compliance. Context7 integration noted for implementation phase.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully with all required artifacts
- Graders run and results (PASS/FAIL): Constitution Check: PASS, Technical Context: PASS, Architecture Decisions: PASS
- Prompt variant (if applicable): Standard /sp.plan workflow
- Next experiment (smallest change to try): Proceed with /sp.tasks to validate task breakdown aligns with plan architecture
