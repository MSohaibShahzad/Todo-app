# Data Model: Phase II Full-Stack Todo Web Application

**Feature**: 003-full-stack-todo-app
**Date**: 2026-01-09
**Database**: Neon Serverless PostgreSQL
**ORM**: SQLModel (Pydantic + SQLAlchemy)

## Overview

This document defines the database schema and data models for the full-stack Todo application. The schema supports multi-user authentication, task management, and all features from Phase-1 (priorities, categories, due dates, recurring tasks).

## Entity Relationship Diagram

```
┌─────────────┐         ┌──────────────────┐
│   User      │ 1     * │      Task        │
│─────────────│◄────────│──────────────────│
│ id (PK)     │         │ id (PK)          │
│ email       │         │ user_id (FK)     │
│ name        │         │ title            │
│ created_at  │         │ description      │
│ updated_at  │         │ completed        │
└─────────────┘         │ priority         │
                        │ category         │
                        │ due_date         │
                        │ recurrence       │
                        │ created_at       │
                        │ updated_at       │
                        └──────────────────┘

Relationship: One user has many tasks (1:N)
Constraint: Each task must belong to exactly one user
```

---

## Table Definitions

### Table: `users`

**Purpose**: Store user account information for authentication and task ownership.

**Note**: This table is managed by Better Auth. The schema below represents the expected structure. Better Auth may add additional fields (password_hash, email_verified, etc.).

| Column       | Type      | Constraints                  | Description                          |
|--------------|-----------|------------------------------|--------------------------------------|
| `id`         | TEXT      | PRIMARY KEY                  | Unique user identifier (UUID)        |
| `email`      | TEXT      | UNIQUE, NOT NULL             | User's email address                 |
| `name`       | TEXT      | NULL                         | User's display name                  |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW()      | Account creation timestamp           |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW()      | Last account update timestamp        |

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` (automatic, enforces uniqueness)

**Validation Rules**:
- `email`: Must be valid email format (validated by Better Auth)
- `email`: Case-insensitive uniqueness (Better Auth handles this)

---

### Table: `tasks`

**Purpose**: Store all task data for all users with multi-tenant isolation.

| Column        | Type      | Constraints                    | Description                                      |
|---------------|-----------|--------------------------------|--------------------------------------------------|
| `id`          | INTEGER   | PRIMARY KEY, AUTOINCREMENT     | Unique task identifier                           |
| `user_id`     | TEXT      | NOT NULL, FOREIGN KEY → users  | Owner of the task (multi-tenancy isolation)      |
| `title`       | TEXT      | NOT NULL                       | Task title (1-200 characters, validated in app)  |
| `description` | TEXT      | NULL                           | Optional task description (max 1000 chars)       |
| `completed`   | BOOLEAN   | NOT NULL, DEFAULT FALSE        | Completion status                                |
| `priority`    | TEXT      | NOT NULL, DEFAULT 'medium'     | Priority level: 'low', 'medium', 'high'          |
| `category`    | TEXT      | NULL                           | Optional category label (e.g., 'Work', 'Personal')|
| `due_date`    | DATE      | NULL                           | Optional due date for the task                   |
| `recurrence`  | TEXT      | NOT NULL, DEFAULT 'none'       | Recurrence pattern: 'none', 'daily', 'weekly', 'monthly' |
| `created_at`  | TIMESTAMP | NOT NULL, DEFAULT NOW()        | Task creation timestamp                          |
| `updated_at`  | TIMESTAMP | NOT NULL, DEFAULT NOW()        | Last update timestamp                            |

**Indexes**:
- Primary key index on `id` (automatic)
- **Index on `user_id`** (critical for multi-tenant queries): `idx_tasks_user_id`
- **Index on `completed`** (for status filtering): `idx_tasks_completed`
- **Index on `priority`** (for priority filtering): `idx_tasks_priority`
- **Index on `due_date`** (for overdue/due-today queries): `idx_tasks_due_date`
- **Composite index on `(user_id, completed)`** (common query pattern): `idx_tasks_user_status`

**Foreign Keys**:
- `user_id` references `users(id)` with `ON DELETE CASCADE`
  - Rationale: If a user account is deleted, all their tasks should be deleted automatically

---

## Enumerations

### Priority Levels

```python
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

**Display Mapping**:
- `LOW`: Blue indicator, normal text
- `MEDIUM`: Yellow indicator, normal text
- `HIGH`: Red indicator, bold text

---

### Recurrence Patterns

```python
class Recurrence(str, Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
```

**Behavior**:
- `NONE`: Task does not recur
- `DAILY`: When completed, creates new task with `due_date + 1 day`
- `WEEKLY`: When completed, creates new task with `due_date + 7 days`
- `MONTHLY`: When completed, creates new task with `due_date + 1 month` (same day of month)

---

## SQLModel Definitions

### User Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    """User account model (managed by Better Auth)"""
    __tablename__ = "users"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Note**: Better Auth will handle additional fields like `password_hash`, `email_verified`, etc.

---

### Task Model (Database)

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date
from typing import Optional
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Recurrence(str, Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class Task(SQLModel, table=True):
    """Task model for database persistence"""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True, nullable=False)
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, nullable=False)
    priority: Priority = Field(default=Priority.MEDIUM, nullable=False)
    category: Optional[str] = Field(default=None, max_length=50)
    due_date: Optional[date] = None
    recurrence: Recurrence = Field(default=Recurrence.NONE, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (optional, for eager loading)
    # user: Optional[User] = Relationship(back_populates="tasks")
```

---

### Pydantic Schemas (API Layer)

These models are used for API request/response validation and serialization.

#### TaskCreate (Request)

```python
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Priority = Priority.MEDIUM
    category: Optional[str] = Field(None, max_length=50)
    due_date: Optional[date] = None
    recurrence: Recurrence = Recurrence.NONE

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": "high",
                "category": "Personal",
                "due_date": "2026-01-10",
                "recurrence": "none"
            }
        }
```

#### TaskUpdate (Request)

```python
class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[Priority] = None
    category: Optional[str] = Field(None, max_length=50)
    due_date: Optional[date] = None
    recurrence: Optional[Recurrence] = None
    completed: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries and cook dinner",
                "priority": "medium",
                "completed": True
            }
        }
```

#### TaskResponse (Response)

```python
class TaskResponse(BaseModel):
    """Schema for task responses (includes all fields + metadata)"""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: Priority
    category: Optional[str]
    due_date: Optional[date]
    recurrence: Recurrence
    created_at: datetime
    updated_at: datetime

    # Computed fields (for frontend convenience)
    is_overdue: bool = False
    is_due_today: bool = False

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel conversion

    @classmethod
    def from_orm_with_status(cls, task: Task) -> "TaskResponse":
        """Create response with computed status fields"""
        from datetime import date
        today = date.today()
        is_overdue = task.due_date is not None and task.due_date < today and not task.completed
        is_due_today = task.due_date == today and not task.completed

        return cls(
            **task.model_dump(),
            is_overdue=is_overdue,
            is_due_today=is_due_today
        )
```

---

## Validation Rules

### Task Title
- **Required**: Cannot be empty
- **Min Length**: 1 character
- **Max Length**: 200 characters
- **Validation**: Frontend and backend validate length

### Task Description
- **Optional**: Can be null/empty
- **Max Length**: 1000 characters
- **Validation**: Backend validates if provided

### Priority
- **Values**: Must be one of `low`, `medium`, `high`
- **Default**: `medium` if not specified
- **Validation**: Enum validation on backend

### Category
- **Optional**: Can be null
- **Max Length**: 50 characters
- **Format**: Free-form text, case-sensitive
- **Validation**: No predefined list; user can create any category

### Due Date
- **Optional**: Can be null
- **Format**: ISO 8601 date (YYYY-MM-DD)
- **Validation**: Must be a valid date (can be in the past)

### Recurrence
- **Values**: Must be one of `none`, `daily`, `weekly`, `monthly`
- **Default**: `none` if not specified
- **Validation**: Enum validation on backend

---

## Database Migrations

### Initial Schema (Migration 001)

```sql
-- Create users table (Better Auth will manage this, but for reference)
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create tasks table
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    priority TEXT NOT NULL DEFAULT 'medium',
    category TEXT,
    due_date DATE,
    recurrence TEXT NOT NULL DEFAULT 'none',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_user_status ON tasks(user_id, completed);
```

**Migration Tool**: Use Alembic for database migrations

---

## Query Patterns

### 1. Get All Tasks for User (with filters)

```python
async def get_user_tasks(
    db: AsyncSession,
    user_id: str,
    status: Optional[str] = None,
    priority: Optional[Priority] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> list[Task]:
    """
    Fetch tasks for a specific user with optional filtering and sorting.
    This is the most common query pattern in the application.
    """
    query = select(Task).where(Task.user_id == user_id)

    # Filter by completion status
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    # Filter by priority
    if priority:
        query = query.where(Task.priority == priority)

    # Filter by category
    if category:
        query = query.where(Task.category == category)

    # Search in title and description
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )

    # Sorting
    sort_column = getattr(Task, sort_by, Task.created_at)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    result = await db.execute(query)
    return result.scalars().all()
```

**Performance**: Indexed on `user_id`, `completed`, `priority` for optimal filtering

---

### 2. Get Overdue Tasks

```python
async def get_overdue_tasks(db: AsyncSession, user_id: str) -> list[Task]:
    """Get all incomplete tasks that are past their due date"""
    from datetime import date
    today = date.today()

    query = select(Task).where(
        Task.user_id == user_id,
        Task.completed == False,
        Task.due_date < today,
        Task.due_date.is_not(None)
    ).order_by(Task.due_date.asc())

    result = await db.execute(query)
    return result.scalars().all()
```

**Performance**: Indexed on `due_date` for efficient date comparisons

---

### 3. Get Tasks Due Today

```python
async def get_tasks_due_today(db: AsyncSession, user_id: str) -> list[Task]:
    """Get all incomplete tasks due today"""
    from datetime import date
    today = date.today()

    query = select(Task).where(
        Task.user_id == user_id,
        Task.completed == False,
        Task.due_date == today
    ).order_by(Task.priority.desc())

    result = await db.execute(query)
    return result.scalars().all()
```

---

### 4. Create Recurring Task Instance

```python
async def create_recurring_task_instance(
    db: AsyncSession,
    original_task: Task
) -> Task:
    """
    When a recurring task is marked complete, create a new instance
    with the next due date based on recurrence pattern.
    """
    from datetime import timedelta
    from dateutil.relativedelta import relativedelta

    if original_task.recurrence == Recurrence.NONE:
        return None

    # Calculate next due date
    next_due_date = original_task.due_date
    if original_task.recurrence == Recurrence.DAILY:
        next_due_date = original_task.due_date + timedelta(days=1)
    elif original_task.recurrence == Recurrence.WEEKLY:
        next_due_date = original_task.due_date + timedelta(weeks=1)
    elif original_task.recurrence == Recurrence.MONTHLY:
        next_due_date = original_task.due_date + relativedelta(months=1)

    # Create new task instance
    new_task = Task(
        user_id=original_task.user_id,
        title=original_task.title,
        description=original_task.description,
        priority=original_task.priority,
        category=original_task.category,
        due_date=next_due_date,
        recurrence=original_task.recurrence,
        completed=False
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task
```

---

## Data Isolation & Security

### User Data Isolation

**Critical Requirement**: Users must NEVER be able to access tasks belonging to other users.

**Implementation**:
1. **All queries include `user_id` filter**:
   ```python
   query = select(Task).where(Task.user_id == user_id)
   ```

2. **Extract `user_id` from JWT** (not from request body):
   ```python
   @router.get("/api/tasks")
   async def list_tasks(
       user_id: str = Depends(get_current_user),  # From JWT
       db: AsyncSession = Depends(get_db)
   ):
       tasks = await get_user_tasks(db, user_id)
       return tasks
   ```

3. **Verify ownership before updates/deletes**:
   ```python
   async def delete_task(db: AsyncSession, task_id: int, user_id: str) -> bool:
       task = await db.get(Task, task_id)
       if task is None:
           raise HTTPException(status_code=404, detail="Task not found")
       if task.user_id != user_id:
           raise HTTPException(status_code=403, detail="Not authorized")
       await db.delete(task)
       await db.commit()
       return True
   ```

---

## Testing Considerations

### Data Isolation Tests

```python
@pytest.mark.asyncio
async def test_user_cannot_access_other_users_tasks():
    """Critical security test: verify user data isolation"""
    # Create two users and their tasks
    user1_task = await create_task(db, user_id="user1", title="User 1 Task")
    user2_task = await create_task(db, user_id="user2", title="User 2 Task")

    # User 1 should only see their own task
    user1_tasks = await get_user_tasks(db, user_id="user1")
    assert len(user1_tasks) == 1
    assert user1_tasks[0].title == "User 1 Task"

    # User 2 should only see their own task
    user2_tasks = await get_user_tasks(db, user_id="user2")
    assert len(user2_tasks) == 1
    assert user2_tasks[0].title == "User 2 Task"

@pytest.mark.asyncio
async def test_user_cannot_delete_other_users_task():
    """Verify authorization on delete operations"""
    user1_task = await create_task(db, user_id="user1", title="User 1 Task")

    # User 2 attempts to delete User 1's task
    with pytest.raises(HTTPException) as exc:
        await delete_task(db, task_id=user1_task.id, user_id="user2")
    assert exc.value.status_code == 403
```

---

## Migration from Phase-1 Console App

### Mapping: Console App → Database

| Console App (In-Memory) | Database (SQLModel) | Changes |
|-------------------------|---------------------|---------|
| `Task.id` (auto-increment) | `Task.id` (INTEGER PK) | Same concept, database-managed |
| No user concept | `Task.user_id` (TEXT FK) | **NEW**: Multi-tenant support |
| `Task.title` (str) | `Task.title` (TEXT NOT NULL) | Same, added length constraints |
| `Task.description` (str \| None) | `Task.description` (TEXT NULL) | Same |
| `Task.completed` (bool) | `Task.completed` (BOOLEAN) | Same |
| `Task.priority` (Priority enum) | `Task.priority` (TEXT, enum validated) | Same enum, stored as text |
| `Task.category` (str \| None) | `Task.category` (TEXT NULL) | Same |
| `Task.due_date` (date \| None) | `Task.due_date` (DATE NULL) | Same |
| `Task.recurrence` (Recurrence enum) | `Task.recurrence` (TEXT, enum validated) | Same enum |
| No timestamp | `Task.created_at` (TIMESTAMP) | **NEW**: Audit trail |
| No timestamp | `Task.updated_at` (TIMESTAMP) | **NEW**: Audit trail |

**Code Reuse**: ~90% of validation logic can be reused directly from Phase-1 models

---

## Summary

**Entities**: 2 (User, Task)
**Relationships**: 1:N (User → Tasks)
**Indexes**: 6 (including 1 composite index)
**Validation**: Pydantic models for API layer, SQLModel for database
**Security**: User data isolation via `user_id` filtering on all queries
**Performance**: Optimized indexes for common query patterns (user, status, priority, due date)

**Next Steps**: Generate API contracts (OpenAPI spec) based on these models
