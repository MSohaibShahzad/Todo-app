# API Contracts: Phase II Full-Stack Todo Web Application

**Feature**: 003-full-stack-todo-app
**Date**: 2026-01-09
**API Version**: 1.0.0

## Overview

This directory contains the API contracts for the full-stack Todo application. The contracts define the interface between the Next.js frontend and FastAPI backend.

## Files

- **`openapi.yaml`**: Complete OpenAPI 3.1 specification for all API endpoints
- **`README.md`**: This file - contract summary and usage guide

## API Base URLs

| Environment | URL |
|-------------|-----|
| Development | `http://localhost:8000` |
| Production | `https://api.todo-app.example.com` |

## Authentication

All task-related endpoints require authentication using JWT Bearer tokens.

**Header Format**:
```
Authorization: Bearer <jwt_token>
```

**Token Source**: JWT tokens are obtained from Better Auth on the frontend and included in all API requests.

**Unauthenticated Endpoints**:
- `GET /health` - Health check (no auth required)

## Endpoints Summary

### Health Check

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/health` | API health check | No |

### Task Management

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/tasks` | List all user's tasks (with filtering) | Yes |
| POST | `/api/tasks` | Create a new task | Yes |
| GET | `/api/tasks/{task_id}` | Get a specific task | Yes |
| PUT | `/api/tasks/{task_id}` | Update a task | Yes |
| DELETE | `/api/tasks/{task_id}` | Delete a task | Yes |
| PATCH | `/api/tasks/{task_id}/complete` | Toggle task completion | Yes |
| GET | `/api/tasks/summary` | Get task statistics | Yes |

## Request Examples

### 1. Create Task

**Request**:
```http
POST /api/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, cheese",
  "priority": "high",
  "category": "Personal",
  "due_date": "2026-01-15",
  "recurrence": "none"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, cheese",
  "completed": false,
  "priority": "high",
  "category": "Personal",
  "due_date": "2026-01-15",
  "recurrence": "none",
  "created_at": "2026-01-09T12:00:00Z",
  "updated_at": "2026-01-09T12:00:00Z",
  "is_overdue": false,
  "is_due_today": false
}
```

---

### 2. List Tasks with Filters

**Request**:
```http
GET /api/tasks?status=pending&priority=high&sort_by=due_date&sort_order=asc
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": "user_abc123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "priority": "high",
    "category": "Personal",
    "due_date": "2026-01-15",
    "recurrence": "none",
    "created_at": "2026-01-09T12:00:00Z",
    "updated_at": "2026-01-09T12:00:00Z",
    "is_overdue": false,
    "is_due_today": false
  },
  {
    "id": 5,
    "user_id": "user_abc123",
    "title": "Finish project report",
    "description": "Complete sections 3-5",
    "completed": false,
    "priority": "high",
    "category": "Work",
    "due_date": "2026-01-20",
    "recurrence": "none",
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T10:00:00Z",
    "is_overdue": false,
    "is_due_today": false
  }
]
```

---

### 3. Update Task

**Request**:
```http
PUT /api/tasks/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries and prepare dinner",
  "priority": "medium",
  "completed": true
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Buy groceries and prepare dinner",
  "description": "Milk, eggs, bread, cheese",
  "completed": true,
  "priority": "medium",
  "category": "Personal",
  "due_date": "2026-01-15",
  "recurrence": "none",
  "created_at": "2026-01-09T12:00:00Z",
  "updated_at": "2026-01-09T14:30:00Z",
  "is_overdue": false,
  "is_due_today": false
}
```

---

### 4. Mark Task Complete (Recurring Task)

**Request**:
```http
PATCH /api/tasks/3/complete
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "completed": true
}
```

**Response** (200 OK):
```json
{
  "task": {
    "id": 3,
    "user_id": "user_abc123",
    "title": "Daily standup meeting",
    "description": "Team sync at 9 AM",
    "completed": true,
    "priority": "medium",
    "category": "Work",
    "due_date": "2026-01-09",
    "recurrence": "daily",
    "created_at": "2026-01-01T08:00:00Z",
    "updated_at": "2026-01-09T15:00:00Z",
    "is_overdue": false,
    "is_due_today": false
  },
  "recurring_task_created": true,
  "new_task": {
    "id": 15,
    "user_id": "user_abc123",
    "title": "Daily standup meeting",
    "description": "Team sync at 9 AM",
    "completed": false,
    "priority": "medium",
    "category": "Work",
    "due_date": "2026-01-10",
    "recurrence": "daily",
    "created_at": "2026-01-09T15:00:00Z",
    "updated_at": "2026-01-09T15:00:00Z",
    "is_overdue": false,
    "is_due_today": false
  }
}
```

---

### 5. Get Task Summary

**Request**:
```http
GET /api/tasks/summary
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response** (200 OK):
```json
{
  "total": 25,
  "pending": 18,
  "completed": 7,
  "overdue": 3,
  "due_today": 5,
  "due_tomorrow": 2
}
```

---

### 6. Delete Task

**Request**:
```http
DELETE /api/tasks/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response** (204 No Content):
```
(empty body)
```

---

## Query Parameters (GET /api/tasks)

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `status` | string | `all`, `pending`, `completed` | Filter by completion status (default: `all`) |
| `priority` | string | `low`, `medium`, `high` | Filter by priority level |
| `category` | string | any | Filter by exact category match |
| `search` | string | any | Search in title and description (case-insensitive) |
| `sort_by` | string | `created_at`, `title`, `priority`, `due_date` | Field to sort by (default: `created_at`) |
| `sort_order` | string | `asc`, `desc` | Sort direction (default: `desc`) |

**Examples**:
- Get all pending tasks: `?status=pending`
- Get high priority tasks: `?priority=high`
- Get work tasks: `?category=Work`
- Search for "groceries": `?search=groceries`
- Get pending high priority tasks sorted by due date: `?status=pending&priority=high&sort_by=due_date&sort_order=asc`

---

## Error Responses

### 400 Bad Request (Validation Error)

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 401 Unauthorized

```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden

```json
{
  "detail": "Not authorized to access this task"
}
```

### 404 Not Found

```json
{
  "detail": "Task not found"
}
```

### 500 Internal Server Error

```json
{
  "detail": "An unexpected error occurred"
}
```

---

## Data Validation Rules

### Task Title
- **Required**: Yes
- **Min Length**: 1 character
- **Max Length**: 200 characters
- **Type**: string

### Task Description
- **Required**: No
- **Max Length**: 1000 characters
- **Type**: string or null

### Priority
- **Required**: No (defaults to `medium`)
- **Values**: `low`, `medium`, `high`
- **Type**: string (enum)

### Category
- **Required**: No
- **Max Length**: 50 characters
- **Type**: string or null

### Due Date
- **Required**: No
- **Format**: ISO 8601 date (YYYY-MM-DD)
- **Type**: string (date) or null

### Recurrence
- **Required**: No (defaults to `none`)
- **Values**: `none`, `daily`, `weekly`, `monthly`
- **Type**: string (enum)

---

## Authentication Flow

### Frontend Responsibilities
1. User signs up/signs in via Better Auth
2. Better Auth returns JWT token
3. Frontend stores token securely (httpOnly cookie or secure storage)
4. Frontend includes token in `Authorization` header for all API requests

### Backend Responsibilities
1. Extract JWT token from `Authorization` header
2. Verify token signature and expiration
3. Extract `user_id` from token payload
4. Inject `user_id` into route handler via dependency injection
5. Return 401 if token is missing, invalid, or expired

### Token Format

```
Authorization: Bearer <token>
```

Where `<token>` is a JWT with the following structure:

```json
{
  "sub": "user_abc123",  // User ID
  "exp": 1704815600,     // Expiration timestamp
  "iat": 1704729200      // Issued at timestamp
}
```

---

## CORS Configuration

**Development**:
- Allowed Origins: `http://localhost:3000` (Next.js dev server)

**Production**:
- Allowed Origins: `https://todo-app.example.com` (frontend domain)

**Allowed Methods**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `OPTIONS`

**Allowed Headers**: `Content-Type`, `Authorization`

---

## Rate Limiting

**Recommendations**:
- Authentication endpoints: 5 requests/minute per IP
- Task endpoints: 100 requests/minute per user
- Health check: Unlimited

**Implementation**: Use `slowapi` or similar middleware on FastAPI

---

## Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Create task (with auth)
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "priority": "high"}'

# List tasks
curl http://localhost:8000/api/tasks?status=pending \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Using Swagger UI

FastAPI automatically generates Swagger UI documentation:

**URL**: `http://localhost:8000/docs`

Features:
- Interactive API testing
- Request/response examples
- Schema definitions
- Try it out functionality

---

## Frontend Integration Example

### TypeScript API Client

```typescript
// lib/api/tasks.ts
import { apiRequest } from './client';

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  category: string | null;
  due_date: string | null;
  recurrence: 'none' | 'daily' | 'weekly' | 'monthly';
  created_at: string;
  updated_at: string;
  is_overdue: boolean;
  is_due_today: boolean;
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  category?: string;
  due_date?: string;
  recurrence?: 'none' | 'daily' | 'weekly' | 'monthly';
}

export async function getTasks(filters?: {
  status?: 'all' | 'pending' | 'completed';
  priority?: 'low' | 'medium' | 'high';
  category?: string;
  search?: string;
  sort_by?: 'created_at' | 'title' | 'priority' | 'due_date';
  sort_order?: 'asc' | 'desc';
}): Promise<Task[]> {
  const params = new URLSearchParams(filters as any);
  return apiRequest<Task[]>(`/api/tasks?${params}`);
}

export async function createTask(data: TaskCreate): Promise<Task> {
  return apiRequest<Task>('/api/tasks', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateTask(id: number, data: Partial<TaskCreate>): Promise<Task> {
  return apiRequest<Task>(`/api/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteTask(id: number): Promise<void> {
  return apiRequest<void>(`/api/tasks/${id}`, {
    method: 'DELETE',
  });
}

export async function toggleTaskComplete(id: number, completed: boolean): Promise<{
  task: Task;
  recurring_task_created: boolean;
  new_task: Task | null;
}> {
  return apiRequest(`/api/tasks/${id}/complete`, {
    method: 'PATCH',
    body: JSON.stringify({ completed }),
  });
}

export async function getTasksSummary(): Promise<{
  total: number;
  pending: number;
  completed: number;
  overdue: number;
  due_today: number;
  due_tomorrow: number;
}> {
  return apiRequest('/api/tasks/summary');
}
```

---

## Contract Versioning

**Current Version**: 1.0.0

**Versioning Strategy**:
- Breaking changes: Increment major version (e.g., 1.0.0 → 2.0.0)
- New features: Increment minor version (e.g., 1.0.0 → 1.1.0)
- Bug fixes: Increment patch version (e.g., 1.0.0 → 1.0.1)

**API Versioning** (future consideration):
- Include version in URL: `/api/v1/tasks`
- Or use Accept header: `Accept: application/vnd.todoapp.v1+json`

---

## Next Steps

1. Implement backend routes based on this contract
2. Generate TypeScript types from OpenAPI spec (using openapi-typescript)
3. Add contract tests to verify backend matches specification
4. Implement frontend API client using these contracts
5. Set up Swagger UI for API documentation
