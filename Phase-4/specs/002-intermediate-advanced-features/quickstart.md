# Quickstart: Implementing Intermediate & Advanced Features

## Overview
This quickstart guide provides step-by-step instructions for implementing Phase-2 features (intermediate and advanced task management) for the Todo console application.

**Target Audience**: Developers implementing the feature
**Prerequisites**: Phase-1 (Basic Todo App) completed and tested
**Estimated Effort**: 3-5 days (following TDD Red-Green-Refactor)

---

## Implementation Phases

### Phase 0: Setup & Preparation ✓
**Status**: Complete (research.md, data-model.md, contracts)

**Artifacts**:
- `research.md` - Architectural decisions and rationale
- `data-model.md` - Extended Task model and validation rules
- `contracts/` - Service and CLI interface contracts

---

### Phase 1: Extend Task Model (TDD)

#### 1.1 Write Tests (RED)
**File**: `tests/unit/test_task_model.py`

Add tests for new Task fields:
```python
def test_task_with_priority():
    """Test task creation with priority field."""
    task = Task(id=1, title="Test", priority="high")
    assert task.priority == "high"

def test_task_with_invalid_priority_raises_error():
    """Test that invalid priority raises ValueError."""
    # This will be validated in TaskManager, not Task dataclass
    # Task model is just data structure
    pass

def test_task_with_category():
    """Test task creation with category field."""
    task = Task(id=1, title="Test", category="Work")
    assert task.category == "Work"

def test_task_with_due_date():
    """Test task creation with due date."""
    due = datetime(2026, 1, 15, 12, 0)
    task = Task(id=1, title="Test", due_date=due)
    assert task.due_date == due

def test_task_with_recurrence_rule():
    """Test task creation with recurrence rule."""
    task = Task(id=1, title="Test", recurrence_rule="daily")
    assert task.recurrence_rule == "daily"

def test_task_defaults_for_phase2_fields():
    """Test that Phase-2 fields default to None."""
    task = Task(id=1, title="Test")
    assert task.priority is None
    assert task.category is None
    assert task.due_date is None
    assert task.recurrence_rule is None
```

**Run tests**: `pytest tests/unit/test_task_model.py -v`
**Expected**: All tests FAIL (RED phase)

#### 1.2 Implement Task Model Extension (GREEN)
**File**: `src/models/task.py`

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a single todo item with intermediate/advanced features."""
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

**Run tests**: `pytest tests/unit/test_task_model.py -v`
**Expected**: All tests PASS (GREEN phase)

#### 1.3 Refactor (if needed)
No refactoring needed for simple dataclass extension.

---

### Phase 2: Extend TaskManager Service (TDD)

#### 2.1 Add Validation Constants
**File**: `src/services/task_manager.py`

```python
# Add after existing constants
VALID_PRIORITIES = {"low", "medium", "high"}
VALID_RECURRENCE_RULES = {"daily", "weekly", "monthly"}
MAX_CATEGORY_LENGTH = 50
```

#### 2.2 Write Tests for add_task() Extension (RED)
**File**: `tests/unit/test_task_manager.py`

```python
def test_add_task_with_priority():
    """Test adding task with priority."""
    manager = TaskManager()
    task = manager.add_task("Test", priority="high")
    assert task.priority == "high"

def test_add_task_with_invalid_priority_raises_error():
    """Test that invalid priority raises ValueError."""
    manager = TaskManager()
    with pytest.raises(ValueError, match="Priority must be"):
        manager.add_task("Test", priority="urgent")

def test_add_task_with_category():
    """Test adding task with category."""
    manager = TaskManager()
    task = manager.add_task("Test", category="Work")
    assert task.category == "Work"

def test_add_task_with_category_too_long_raises_error():
    """Test that category > 50 chars raises ValueError."""
    manager = TaskManager()
    long_category = "A" * 51
    with pytest.raises(ValueError, match="Category exceeds"):
        manager.add_task("Test", category=long_category)

def test_add_task_with_due_date():
    """Test adding task with due date."""
    manager = TaskManager()
    future = datetime.now() + timedelta(days=1)
    task = manager.add_task("Test", due_date=future)
    assert task.due_date == future

def test_add_task_with_past_due_date_raises_error():
    """Test that past due date raises ValueError."""
    manager = TaskManager()
    past = datetime.now() - timedelta(days=1)
    with pytest.raises(ValueError, match="Due date must be in the future"):
        manager.add_task("Test", due_date=past)

def test_add_task_with_recurrence_rule():
    """Test adding task with recurrence rule."""
    manager = TaskManager()
    task = manager.add_task("Test", recurrence_rule="daily")
    assert task.recurrence_rule == "daily"

def test_add_task_with_invalid_recurrence_raises_error():
    """Test that invalid recurrence rule raises ValueError."""
    manager = TaskManager()
    with pytest.raises(ValueError, match="Recurrence rule must be"):
        manager.add_task("Test", recurrence_rule="hourly")
```

**Run tests**: `pytest tests/unit/test_task_manager.py::test_add_task_with_priority -v`
**Expected**: FAIL (RED phase)

#### 2.3 Implement add_task() Validation (GREEN)
**File**: `src/services/task_manager.py`

Extend `add_task()` method:
```python
def add_task(
    self,
    title: str,
    description: str = "",
    priority: Optional[str] = None,
    category: Optional[str] = None,
    due_date: Optional[datetime] = None,
    recurrence_rule: Optional[str] = None
) -> Task:
    """Add a new task to the manager (Phase-2 extended)."""
    # Existing Phase-1 validation
    title = title.strip()
    if not title:
        raise ValueError("Title cannot be empty")
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"Title exceeds maximum length of {MAX_TITLE_LENGTH} characters")
    if len(description) > MAX_DESCRIPTION_LENGTH:
        raise ValueError(f"Description exceeds maximum length of {MAX_DESCRIPTION_LENGTH} characters")

    # Phase-2 validation
    if priority is not None and priority not in VALID_PRIORITIES:
        raise ValueError(f"Priority must be one of {VALID_PRIORITIES} or None")

    if category is not None:
        if len(category) > MAX_CATEGORY_LENGTH:
            raise ValueError(f"Category exceeds maximum length of {MAX_CATEGORY_LENGTH} characters")
        if not category.strip():
            raise ValueError("Category cannot be empty or whitespace-only")

    if due_date is not None and due_date <= datetime.now():
        raise ValueError("Due date must be in the future")

    if recurrence_rule is not None and recurrence_rule not in VALID_RECURRENCE_RULES:
        raise ValueError(f"Recurrence rule must be one of {VALID_RECURRENCE_RULES} or None")

    # Create task with Phase-2 fields
    task = Task(
        id=self.next_id,
        title=title,
        description=description,
        is_complete=False,
        priority=priority,
        category=category,
        due_date=due_date,
        recurrence_rule=recurrence_rule
    )

    self.tasks[self.next_id] = task
    self.next_id += 1

    return task
```

**Run tests**: `pytest tests/unit/test_task_manager.py -v`
**Expected**: All tests PASS (GREEN phase)

---

### Phase 3: Implement Search & Filter (TDD)

#### 3.1 Write Tests for search_tasks() (RED)
**File**: `tests/unit/test_task_filtering.py` (new file)

```python
import pytest
from src.services.task_manager import TaskManager


def test_search_tasks_by_title():
    """Test searching tasks by title keyword."""
    manager = TaskManager()
    manager.add_task("Buy groceries")
    manager.add_task("Buy books")
    manager.add_task("Read documentation")

    results = manager.search_tasks("buy")
    assert len(results) == 2
    assert all("buy" in task.title.lower() for task in results)


def test_search_tasks_by_description():
    """Test searching tasks by description keyword."""
    manager = TaskManager()
    manager.add_task("Task 1", description="Important meeting")
    manager.add_task("Task 2", description="Casual chat")
    manager.add_task("Task 3", description="Team meeting")

    results = manager.search_tasks("meeting")
    assert len(results) == 2


def test_search_tasks_case_insensitive():
    """Test that search is case-insensitive."""
    manager = TaskManager()
    manager.add_task("URGENT Task")

    results = manager.search_tasks("urgent")
    assert len(results) == 1


def test_search_tasks_no_matches():
    """Test search with no matching tasks."""
    manager = TaskManager()
    manager.add_task("Task 1")

    results = manager.search_tasks("nonexistent")
    assert len(results) == 0
```

**Run tests**: `pytest tests/unit/test_task_filtering.py -v`
**Expected**: FAIL (RED phase)

#### 3.2 Implement search_tasks() (GREEN)
**File**: `src/services/task_manager.py`

```python
def search_tasks(self, query: str) -> List[Task]:
    """Search tasks by keyword (case-insensitive)."""
    query_lower = query.lower()
    results = [
        task for task in self.tasks.values()
        if query_lower in task.title.lower() or query_lower in task.description.lower()
    ]
    return sorted(results, key=lambda t: t.id)
```

**Run tests**: `pytest tests/unit/test_task_filtering.py -v`
**Expected**: All tests PASS (GREEN phase)

#### 3.3 Write Tests for filter_tasks() (RED)
**File**: `tests/unit/test_task_filtering.py`

```python
def test_filter_tasks_by_priority():
    """Test filtering tasks by priority."""
    manager = TaskManager()
    manager.add_task("Task 1", priority="high")
    manager.add_task("Task 2", priority="low")
    manager.add_task("Task 3", priority="high")

    results = manager.filter_tasks(priority="high")
    assert len(results) == 2
    assert all(task.priority == "high" for task in results)


def test_filter_tasks_by_category():
    """Test filtering tasks by category."""
    manager = TaskManager()
    manager.add_task("Task 1", category="Work")
    manager.add_task("Task 2", category="Personal")
    manager.add_task("Task 3", category="Work")

    results = manager.filter_tasks(category="Work")
    assert len(results) == 2


def test_filter_tasks_by_completion_status():
    """Test filtering tasks by completion status."""
    manager = TaskManager()
    t1 = manager.add_task("Task 1")
    t2 = manager.add_task("Task 2")
    manager.mark_complete(t1.id, True)

    results = manager.filter_tasks(is_complete=False)
    assert len(results) == 1
    assert results[0].id == t2.id


def test_filter_tasks_multiple_criteria():
    """Test filtering with multiple criteria (AND logic)."""
    manager = TaskManager()
    manager.add_task("Task 1", priority="high", category="Work")
    manager.add_task("Task 2", priority="high", category="Personal")
    manager.add_task("Task 3", priority="low", category="Work")

    results = manager.filter_tasks(priority="high", category="Work")
    assert len(results) == 1
    assert results[0].title == "Task 1"
```

**Run tests**: `pytest tests/unit/test_task_filtering.py::test_filter_tasks_by_priority -v`
**Expected**: FAIL (RED phase)

#### 3.4 Implement filter_tasks() (GREEN)
**File**: `src/services/task_manager.py`

```python
def filter_tasks(
    self,
    is_complete: Optional[bool] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None
) -> List[Task]:
    """Filter tasks by criteria (AND logic)."""
    results = list(self.tasks.values())

    if is_complete is not None:
        results = [t for t in results if t.is_complete == is_complete]

    if priority is not None:
        results = [t for t in results if t.priority == priority]

    if category is not None:
        results = [t for t in results if t.category == category]

    return sorted(results, key=lambda t: t.id)
```

**Run tests**: `pytest tests/unit/test_task_filtering.py -v`
**Expected**: All tests PASS (GREEN phase)

---

### Phase 4: Implement Sorting (TDD)

Follow same TDD pattern:
1. Write tests for `sort_tasks()` (RED)
2. Implement `sort_tasks()` (GREEN)
3. Refactor (if needed)

**Implementation hint**: Use Python's `sorted()` with custom key functions for each sort key.

---

### Phase 5: Implement Recurring Tasks (TDD)

This is the most complex feature. Follow TDD rigorously.

#### 5.1 Write Tests for Recurrence Logic (RED)
**File**: `tests/unit/test_recurrence_logic.py` (new file)

```python
def test_mark_recurring_task_complete_creates_new_instance():
    """Test that completing a recurring task creates a new instance."""
    manager = TaskManager()
    due = datetime(2026, 1, 8, 9, 0)
    task = manager.add_task("Daily standup", due_date=due, recurrence_rule="daily")

    manager.mark_complete(task.id, True)

    all_tasks = manager.get_all_tasks()
    assert len(all_tasks) == 2  # Original + new instance

    original = all_tasks[0]
    assert original.is_complete is True

    new_instance = all_tasks[1]
    assert new_instance.is_complete is False
    assert new_instance.due_date == datetime(2026, 1, 9, 9, 0)  # +1 day


def test_weekly_recurrence_calculation():
    """Test that weekly recurrence adds 7 days."""
    manager = TaskManager()
    due = datetime(2026, 1, 8, 14, 0)
    task = manager.add_task("Weekly meeting", due_date=due, recurrence_rule="weekly")

    manager.mark_complete(task.id, True)

    all_tasks = manager.get_all_tasks()
    new_instance = all_tasks[1]
    assert new_instance.due_date == datetime(2026, 1, 15, 14, 0)  # +7 days


def test_monthly_recurrence_calculation():
    """Test that monthly recurrence adds 1 month."""
    manager = TaskManager()
    due = datetime(2026, 1, 15, 10, 0)
    task = manager.add_task("Monthly report", due_date=due, recurrence_rule="monthly")

    manager.mark_complete(task.id, True)

    all_tasks = manager.get_all_tasks()
    new_instance = all_tasks[1]
    assert new_instance.due_date == datetime(2026, 2, 15, 10, 0)  # +1 month
```

#### 5.2 Implement Recurrence Logic (GREEN)
**File**: `src/services/task_manager.py`

Modify `mark_complete()`:
```python
def mark_complete(self, task_id: int, is_complete: bool) -> Task:
    """Mark task as complete or incomplete (Phase-2 extended for recurring tasks)."""
    if task_id not in self.tasks:
        raise ValueError(f"Task not found: {task_id}")

    task = self.tasks[task_id]
    task.is_complete = is_complete

    # Handle recurring task regeneration
    if is_complete and task.recurrence_rule and task.due_date:
        next_due_date = self._calculate_next_due_date(task.due_date, task.recurrence_rule)

        # Create new recurring instance
        self.add_task(
            title=task.title,
            description=task.description,
            priority=task.priority,
            category=task.category,
            due_date=next_due_date,
            recurrence_rule=task.recurrence_rule
        )

    return task


def _calculate_next_due_date(self, current_due: datetime, recurrence: str) -> datetime:
    """Calculate next due date based on recurrence rule."""
    from dateutil.relativedelta import relativedelta

    if recurrence == "daily":
        return current_due + timedelta(days=1)
    elif recurrence == "weekly":
        return current_due + timedelta(weeks=1)
    elif recurrence == "monthly":
        return current_due + relativedelta(months=1)
    else:
        raise ValueError(f"Invalid recurrence rule: {recurrence}")
```

**Note**: Requires `python-dateutil` library for month-end handling
```bash
pip install python-dateutil
```

---

### Phase 6: Implement CLI Extensions

#### 6.1 Add Colorama Dependency
```bash
pip install colorama
```

#### 6.2 Update Menu
**File**: `src/cli/menu.py`

Add new menu options (follow CLI contract in `contracts/cli_interface.md`)

#### 6.3 Update Display
**File**: `src/cli/display.py`

Implement color-coded display, due date indicators, etc.

---

### Phase 7: Integration Testing

**File**: `tests/integration/test_filter_and_sort_workflow.py`

Test complete user workflows:
- Add task with all fields → Filter → Sort → Display
- Search tasks → Update → Verify changes
- Create recurring task → Complete → Verify new instance

---

## Testing Strategy

### Test Execution Order
1. Unit tests for models (`test_task_model.py`)
2. Unit tests for service validation (`test_task_manager.py`)
3. Unit tests for filtering/sorting (`test_task_filtering.py`, `test_task_sorting.py`)
4. Unit tests for recurrence logic (`test_recurrence_logic.py`)
5. Integration tests (`test_filter_and_sort_workflow.py`, `test_recurring_task_workflow.py`)

### Coverage Requirements
```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

**Target**: ≥ 80% coverage for all new code

---

## Architectural Decision Record (ADR) Trigger

After completing Phase 1 (design artifacts), review for architecturally significant decisions:

**Three-Part Test**:
1. **Impact**: Does this have long-term consequences? (YES - data model extension)
2. **Alternatives**: Were multiple approaches considered? (YES - see research.md)
3. **Scope**: Is it cross-cutting? (YES - affects all layers)

**Suggested ADR**:
```
📋 Architectural decision detected: Task Model Extension Strategy
   Document reasoning and tradeoffs? Run `/sp.adr task-model-extension-strategy`
```

---

## Common Pitfalls & Solutions

### Pitfall 1: Breaking Phase-1 Tests
**Solution**: Run Phase-1 tests after every change
```bash
pytest tests/unit/test_task_model.py::test_task_creation
pytest tests/unit/test_task_manager.py::test_add_task
```

### Pitfall 2: Month-End Recurrence Edge Cases
**Solution**: Use `python-dateutil` library (handles Jan 31 → Feb 28 automatically)

### Pitfall 3: Due Date Validation During Update
**Solution**: Only validate due_date > now() for NEW due dates, not existing past-due tasks

### Pitfall 4: Search Performance with Large Lists
**Solution**: Acceptable for console app (<10,000 tasks). If needed, add early exit or pagination in Phase-3.

---

## Verification Checklist

Before marking complete, verify:

- [ ] All Phase-1 tests still pass (no regressions)
- [ ] All new unit tests pass (≥ 80% coverage)
- [ ] Integration tests pass for end-to-end workflows
- [ ] Manual testing: Add task with all fields, search, filter, sort, complete recurring task
- [ ] CLI displays correctly with colors (test with colorama installed and uninstalled)
- [ ] Error messages are user-friendly (not technical stack traces)
- [ ] Code follows PEP 8 (run `black` and `flake8`)
- [ ] Type hints present for all new functions
- [ ] Constitution principles followed (simplicity, separation of concerns, TDD)

---

## Next Steps (Phase-3 Preview)

After completing Phase-2, consider:
- Task analytics (completion rate, average time to complete)
- Smart recommendations (suggest priorities based on patterns)
- Task dependencies (blocking/blocked-by relationships)
- Export/import (CSV, JSON)

**Important**: Do not implement Phase-3 features until Phase-2 is complete and stable.

---

**Quickstart Complete**: Follow this guide to implement intermediate and advanced features systematically using TDD.
