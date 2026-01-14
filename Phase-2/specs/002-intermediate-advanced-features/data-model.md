# Data Model: Intermediate & Advanced Features

## Overview
This document defines the data structures and validation rules for extending the basic Todo app with intermediate and advanced task management features.

---

## 1. Task Entity (Extended)

### Definition
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a single todo item with intermediate/advanced features.

    Phase-1 Attributes (Required):
        id: Unique sequential identifier (int, auto-assigned)
        title: Task summary (str, required, max 200 chars)
        description: Detailed task information (str, optional, max 1000 chars)
        is_complete: Completion status (bool, default False)

    Phase-2 Attributes (Optional):
        priority: Task priority level (Optional[str], "low"|"medium"|"high"|None)
        category: Task category/project (Optional[str], max 50 chars)
        due_date: Task deadline (Optional[datetime], must be future)
        recurrence_rule: Recurrence pattern (Optional[str], "daily"|"weekly"|"monthly"|None)
    """
    # Phase-1 fields
    id: int
    title: str
    description: str = ""
    is_complete: bool = False

    # Phase-2 fields
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence_rule: Optional[str] = None
```

### Field Specifications

#### 1.1 ID (int)
- **Type**: `int`
- **Assignment**: Auto-assigned by TaskManager, sequential starting from 1
- **Uniqueness**: Guaranteed unique within TaskManager instance
- **Immutable**: Never changes after creation
- **Range**: 1 to sys.maxsize

#### 1.2 Title (str)
- **Type**: `str`
- **Required**: Yes
- **Constraints**:
  - Non-empty after stripping whitespace
  - Maximum 200 characters
- **Validation**:
  ```python
  title = title.strip()
  if not title:
      raise ValueError("Title cannot be empty")
  if len(title) > 200:
      raise ValueError("Title exceeds maximum length of 200 characters")
  ```

#### 1.3 Description (str)
- **Type**: `str`
- **Required**: No (default: `""`)
- **Constraints**:
  - Maximum 1000 characters
- **Validation**:
  ```python
  if len(description) > 1000:
      raise ValueError("Description exceeds maximum length of 1000 characters")
  ```

#### 1.4 Is Complete (bool)
- **Type**: `bool`
- **Default**: `False`
- **Values**: `True` (complete) or `False` (incomplete)
- **Behavior**: Can be toggled multiple times

#### 1.5 Priority (Optional[str])
- **Type**: `Optional[str]`
- **Default**: `None`
- **Valid Values**: `"low"`, `"medium"`, `"high"`, `None`
- **Validation**:
  ```python
  VALID_PRIORITIES = {"low", "medium", "high"}

  def validate_priority(priority: Optional[str]) -> None:
      if priority is not None and priority not in VALID_PRIORITIES:
          raise ValueError(f"Priority must be one of {VALID_PRIORITIES} or None")
  ```
- **Display Order**: high > medium > low > None

#### 1.6 Category (Optional[str])
- **Type**: `Optional[str]`
- **Default**: `None`
- **Constraints**:
  - Maximum 50 characters
  - Alphanumeric characters, spaces, hyphens, underscores allowed
- **Validation**:
  ```python
  MAX_CATEGORY_LENGTH = 50

  def validate_category(category: Optional[str]) -> None:
      if category is not None:
          if len(category) > MAX_CATEGORY_LENGTH:
              raise ValueError(f"Category exceeds maximum length of {MAX_CATEGORY_LENGTH} characters")
          if not category.strip():
              raise ValueError("Category cannot be empty or whitespace-only")
  ```

#### 1.7 Due Date (Optional[datetime])
- **Type**: `Optional[datetime]`
- **Default**: `None`
- **Constraints**:
  - Must be a future date/time when set
  - Stored with full datetime precision (includes time)
- **Validation**:
  ```python
  from datetime import datetime

  def validate_due_date(due_date: Optional[datetime]) -> None:
      if due_date is not None:
          if due_date <= datetime.now():
              raise ValueError("Due date must be in the future")
  ```
- **Timezone**: Local timezone only (no timezone support in Phase-2)

#### 1.8 Recurrence Rule (Optional[str])
- **Type**: `Optional[str]`
- **Default**: `None`
- **Valid Values**: `"daily"`, `"weekly"`, `"monthly"`, `None`
- **Validation**:
  ```python
  VALID_RECURRENCE_RULES = {"daily", "weekly", "monthly"}

  def validate_recurrence_rule(recurrence: Optional[str]) -> None:
      if recurrence is not None and recurrence not in VALID_RECURRENCE_RULES:
          raise ValueError(f"Recurrence rule must be one of {VALID_RECURRENCE_RULES} or None")
  ```
- **Behavior**: When a recurring task is marked complete, a new instance is generated

---

## 2. Validation Rules Summary

| **Field** | **Required** | **Max Length** | **Valid Values** | **Additional Rules** |
|-----------|--------------|----------------|------------------|----------------------|
| id | Auto | N/A | int ≥ 1 | Auto-assigned, immutable |
| title | Yes | 200 | Non-empty string | Trimmed, no whitespace-only |
| description | No | 1000 | Any string | Empty string default |
| is_complete | No | N/A | True, False | Default False |
| priority | No | N/A | "low", "medium", "high", None | Case-sensitive |
| category | No | 50 | Alphanumeric + spaces/hyphens | Trimmed, no whitespace-only |
| due_date | No | N/A | Future datetime | Local timezone only |
| recurrence_rule | No | N/A | "daily", "weekly", "monthly", None | Case-sensitive |

---

## 3. State Transitions

### 3.1 Task Creation
```
Initial State: Task does not exist
Action: TaskManager.add_task(title, description, priority, category, due_date, recurrence_rule)
Validation:
  - title: non-empty, ≤ 200 chars
  - description: ≤ 1000 chars
  - priority: in VALID_PRIORITIES or None
  - category: ≤ 50 chars, alphanumeric
  - due_date: future datetime or None
  - recurrence_rule: in VALID_RECURRENCE_RULES or None
Result: Task created with id assigned, is_complete=False
```

### 3.2 Task Completion (Non-Recurring)
```
Current State: Task exists, recurrence_rule=None
Action: TaskManager.mark_complete(task_id, is_complete=True)
Result: Task.is_complete = True
```

### 3.3 Task Completion (Recurring)
```
Current State: Task exists, recurrence_rule != None
Action: TaskManager.mark_complete(task_id, is_complete=True)
Logic:
  1. Mark original task as complete (is_complete = True)
  2. Calculate next_due_date based on recurrence_rule:
     - daily: current_due_date + 1 day
     - weekly: current_due_date + 7 days
     - monthly: current_due_date + 1 month (same day of month)
  3. Create new task with:
     - New ID (auto-assigned)
     - Same title, description, priority, category, recurrence_rule
     - due_date = next_due_date
     - is_complete = False
Result: Original task complete + new recurring instance created
```

### 3.4 Task Update
```
Current State: Task exists
Action: TaskManager.update_task(task_id, **fields)
Validation: Same as creation for updated fields
Result: Task fields updated, id and is_complete unchanged (unless explicitly set)
```

### 3.5 Task Deletion
```
Current State: Task exists
Action: TaskManager.delete_task(task_id)
Result: Task removed from storage
```

---

## 4. Business Rules

### BR-1: Priority Sorting
When displaying tasks sorted by priority:
1. High priority tasks appear first
2. Medium priority tasks appear second
3. Low priority tasks appear third
4. Tasks with no priority (None) appear last

### BR-2: Due Date Categorization
Tasks with due_date are categorized for display:
- **Overdue**: `due_date < now()`
- **Due Today**: `due_date.date() == today()`
- **Upcoming**: `due_date - now() ≤ 3 days`
- **Future**: `due_date - now() > 3 days`

### BR-3: Recurrence Regeneration
- Recurrence calculation uses the **completion date**, not the original due date
- If a daily task due Jan 1 is completed Jan 5, next instance is due Jan 6 (not Jan 2)
- Month-end edge case: Jan 31 → Feb 28 (or Feb 29 in leap year)

### BR-4: Search Scope
Search functionality matches against:
- Task title (case-insensitive)
- Task description (case-insensitive)
- Does NOT search: priority, category, dates

### BR-5: Filter Combination
Multiple filters are applied with AND logic:
- `filter(priority="high", category="Work")` → tasks that are BOTH high priority AND in Work category

---

## 5. Data Integrity Constraints

### C-1: ID Uniqueness
- Each task MUST have a unique ID within the TaskManager instance
- IDs are never reused, even after task deletion

### C-2: No Orphaned References
- All tasks exist only in TaskManager.tasks dictionary
- Deletion removes all references (no dangling pointers)

### C-3: Immutable ID
- Task ID cannot be changed after creation
- Update operations MUST NOT modify task ID

### C-4: Valid Priority Values
- Priority field MUST be one of: "low", "medium", "high", or None
- Invalid values are rejected at service layer

### C-5: Future Due Dates Only
- Due dates MUST be in the future at creation time
- Past due dates become "overdue" naturally as time passes
- Cannot set a new due date in the past

---

## 6. Storage Schema (In-Memory)

### TaskManager.tasks
```python
tasks: Dict[int, Task]

# Example:
{
    1: Task(id=1, title="Buy groceries", description="Milk, eggs, bread",
            is_complete=False, priority="medium", category="Personal",
            due_date=datetime(2026, 1, 10, 18, 0), recurrence_rule=None),

    2: Task(id=2, title="Team standup", description="Daily sync with team",
            is_complete=False, priority="high", category="Work",
            due_date=datetime(2026, 1, 8, 9, 0), recurrence_rule="daily"),

    3: Task(id=3, title="Review PR #42", description="Security updates",
            is_complete=True, priority="high", category="Work",
            due_date=None, recurrence_rule=None)
}
```

### TaskManager.next_id
```python
next_id: int  # Sequential counter, starts at 1, increments after each add_task()
```

---

## 7. Backward Compatibility

### Phase-1 Compatibility
All existing Phase-1 functionality remains unchanged:
- Tasks can be created with only title and description
- New optional fields default to None
- Existing tests continue to pass without modification
- CLI menu includes Phase-1 options as-is

### Migration Path
No migration needed:
- In-memory storage (no persistent data to migrate)
- Existing code using Task(id, title, description, is_complete) continues to work
- New features are additive, not replacements

---

## 8. Performance Characteristics

### Storage Complexity
- **Space**: O(n) where n = number of tasks
- **Task Lookup by ID**: O(1) (dictionary access)
- **Get All Tasks**: O(n log n) (sorted by ID)

### Filter/Search Complexity
- **Search**: O(n) - linear scan through all tasks
- **Filter by field**: O(n) - linear scan
- **Multiple filters**: O(n) - single pass with multiple conditions
- **Sort**: O(n log n) - Python's Timsort algorithm

### Scale Assumptions
- Expected usage: 10-1000 tasks
- Performance acceptable up to 10,000 tasks
- No optimization needed for console app use case

---

**Data Model Complete**: All entities, validations, rules, and constraints defined.
