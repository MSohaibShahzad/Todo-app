# Research: Intermediate & Advanced Features

## Overview
This research document resolves architectural questions for extending the basic Todo app with intermediate and advanced features while maintaining the constitutional principles.

## 1. Task Model Extension Design

### Decision: Extend Task dataclass with optional fields

**Rationale**:
- Maintains backward compatibility (existing Phase-1 code continues to work)
- Dataclasses support default values for new fields
- Clean separation between required (Phase-1) and optional (Phase-2) attributes
- No breaking changes to existing tests or service layer

**Alternatives Considered**:
1. **Create new AdvancedTask class** - Rejected: would require dual storage and type checking
2. **Use composition pattern** - Rejected: over-engineering for simple attribute addition
3. **Dynamic attributes via __dict__** - Rejected: loses type safety and IDE support

**Implementation**:
```python
@dataclass
class Task:
    # Phase-1 fields (required)
    id: int
    title: str
    description: str = ""
    is_complete: bool = False

    # Phase-2 fields (optional)
    priority: Optional[str] = None  # "low", "medium", "high"
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence_rule: Optional[str] = None  # "daily", "weekly", "monthly"
```

---

## 2. Priority Level Design

### Decision: Use string literals with validation

**Rationale**:
- Simple to implement and understand
- Easy to display in console
- Extensible for future priority levels
- Validation ensures data integrity

**Alternatives Considered**:
1. **Enum class** - Considered but adds complexity for a simple 3-value choice
2. **Integer values (1-3)** - Rejected: less readable in code and display
3. **No validation** - Rejected: violates data integrity principles

**Valid Values**: `"low"`, `"medium"`, `"high"`, `None` (unset)

**Validation Logic**:
```python
VALID_PRIORITIES = {"low", "medium", "high"}

def validate_priority(priority: Optional[str]) -> None:
    if priority is not None and priority not in VALID_PRIORITIES:
        raise ValueError(f"Priority must be one of {VALID_PRIORITIES}")
```

---

## 3. Recurrence Rule Design

### Decision: Simple string-based recurrence with regeneration logic

**Rationale**:
- Console app doesn't need complex recurrence (no iCal RFC 5545)
- Three common patterns cover 90% of use cases
- Regeneration on completion keeps logic simple
- No background processes needed (console execution only)

**Alternatives Considered**:
1. **RFC 5545 (iCal) format** - Rejected: massive over-engineering for console app
2. **Cron expressions** - Rejected: too technical for end users
3. **Custom DSL** - Rejected: unnecessary complexity

**Valid Values**: `"daily"`, `"weekly"`, `"monthly"`, `None` (non-recurring)

**Regeneration Logic**:
When a recurring task is marked complete:
1. Create new task with same title, description, priority, category, recurrence_rule
2. Calculate new due_date based on recurrence interval from completion date
3. Original task remains marked as complete (maintains history)

---

## 4. Search & Filter Implementation

### Decision: In-memory filtering with list comprehensions

**Rationale**:
- Constitution mandates in-memory storage
- Python list comprehensions are efficient for small datasets (<10,000 tasks)
- Functional approach keeps code simple and testable
- No external dependencies required

**Alternatives Considered**:
1. **SQLite in-memory database** - Rejected: violates "no database" principle
2. **Pandas DataFrame** - Rejected: heavy dependency for simple filtering
3. **Custom indexing structures** - Rejected: premature optimization

**Filter Operations**:
```python
def filter_tasks(tasks: List[Task], **filters) -> List[Task]:
    """Apply filters to task list.

    Supported filters:
    - is_complete: bool
    - priority: str
    - category: str
    - search_text: str (searches title and description)
    """
    result = tasks

    if 'is_complete' in filters:
        result = [t for t in result if t.is_complete == filters['is_complete']]

    if 'priority' in filters:
        result = [t for t in result if t.priority == filters['priority']]

    if 'category' in filters:
        result = [t for t in result if t.category == filters['category']]

    if 'search_text' in filters:
        search = filters['search_text'].lower()
        result = [t for t in result
                  if search in t.title.lower() or search in t.description.lower()]

    return result
```

**Search Performance**: O(n) for each filter, acceptable for console app use case

---

## 5. Sorting Implementation

### Decision: Sorting applied to display results only, not stored

**Rationale**:
- Tasks maintain creation order (ID-based) in storage
- Sort is a view concern, belongs in display layer
- Multiple sort options without mutating data
- Aligns with separation of concerns principle

**Alternatives Considered**:
1. **Store sort order in TaskManager** - Rejected: couples storage to presentation
2. **Multiple storage lists** - Rejected: data duplication and sync issues

**Sort Keys**:
- `id` (default, creation order)
- `priority` (high → medium → low → None)
- `due_date` (earliest first, None last)
- `title` (alphabetical)
- `category` (grouped view)

**Implementation Location**: CLI display layer (`src/cli/display.py`)

---

## 6. Due Date and Reminder Logic

### Decision: Check due dates during display, show inline indicators

**Rationale**:
- No background processes (console app constraint)
- Users see reminders when they interact with app
- Simple date comparison logic
- No need for persistent notification system

**Alternatives Considered**:
1. **Background daemon process** - Rejected: violates console-only constraint
2. **OS-level notifications** - Rejected: out of scope and platform-dependent
3. **Email reminders** - Rejected: external integration, out of scope

**Reminder Categories**:
- **Overdue**: `due_date < now()` → Red indicator, sorted to top
- **Due Today**: `due_date.date() == today()` → Yellow indicator
- **Upcoming**: `due_date within next 3 days` → Blue indicator
- **Future**: `due_date > 3 days away` → Normal display

**Display Logic**:
```python
def get_due_date_indicator(task: Task) -> str:
    if task.due_date is None:
        return ""

    now = datetime.now()
    if task.due_date < now:
        return "[OVERDUE]"  # Red in terminal
    elif task.due_date.date() == now.date():
        return "[DUE TODAY]"  # Yellow
    elif (task.due_date - now).days <= 3:
        return "[UPCOMING]"  # Blue
    return ""
```

---

## 7. Terminal Display Enhancements

### Decision: Use `colorama` for cross-platform color support

**Rationale**:
- Cross-platform (Windows, Linux, macOS)
- Lightweight and stable
- Constitution allows terminal enhancement libraries
- Simple API, no learning curve

**Alternatives Considered**:
1. **rich library** - Considered, but heavier dependency; may use in Phase-3
2. **ANSI codes directly** - Rejected: not cross-platform, manual escape sequence management
3. **termcolor** - Rejected: less maintained than colorama

**Color Mapping**:
- **Priority High**: Red
- **Priority Medium**: Yellow
- **Priority Low**: Green
- **Overdue**: Red + Bold
- **Due Today**: Yellow + Bold
- **Complete**: Gray/Dim

---

## 8. Input Validation Strategy

### Decision: Validate at service layer, provide clear error messages

**Rationale**:
- Service layer owns business rules
- CLI layer catches exceptions and displays user-friendly messages
- Maintains separation of concerns
- Testable validation logic

**Validation Points**:
1. **Priority**: Must be in `{"low", "medium", "high"}` or None
2. **Category**: Max 50 characters, alphanumeric + spaces
3. **Due Date**: Must be future date (can't set due date in past)
4. **Recurrence Rule**: Must be in `{"daily", "weekly", "monthly"}` or None

**Error Message Format**:
```
❌ Invalid priority 'urgent'. Choose from: low, medium, high
❌ Category name too long (max 50 characters)
❌ Due date must be in the future
```

---

## 9. Menu Structure Extension

### Decision: Add submenu for filters and sorting

**Rationale**:
- Keeps main menu simple (constitutional mandate)
- Groups related operations logically
- Maintains backward compatibility with Phase-1 menu
- Easy to navigate with numbered choices

**Menu Hierarchy**:
```
Main Menu:
1. Add Task
2. View All Tasks
3. Filter/Search Tasks [NEW]
4. Update Task
5. Mark Complete/Incomplete
6. Delete Task
7. Exit

Filter/Search Menu:
1. Search by keyword
2. Filter by status
3. Filter by priority
4. Filter by category
5. Sort results
6. Back to main menu
```

**Implementation**: Extend existing menu.py with new submenu function

---

## 10. Testing Strategy for New Features

### Decision: Unit tests for filters/sorting, integration tests for recurring tasks

**Rationale**:
- Filter/sort are pure functions → perfect for unit tests
- Recurring task logic involves multiple components → integration tests
- Maintains TDD approach from constitution
- Clear separation matches service/CLI architecture

**Test Coverage Requirements**:
- Filter functions: 100% (simple, critical logic)
- Sort functions: 100% (simple, critical logic)
- Recurrence regeneration: 100% (complex, error-prone)
- Display formatting: Spot checks (visual, less critical)

**Test Organization**:
```
tests/unit/
  test_task_filtering.py
  test_task_sorting.py
  test_recurrence_logic.py
  test_validation.py

tests/integration/
  test_filter_and_sort_workflow.py
  test_recurring_task_workflow.py
  test_due_date_reminders.py
```

---

## Summary of Key Decisions

| **Aspect** | **Decision** | **Rationale** |
|------------|--------------|---------------|
| Task Model | Extend dataclass with optional fields | Backward compatible, simple |
| Priority | String literals ("low", "medium", "high") | Readable, validated |
| Recurrence | Simple string rules, regenerate on complete | Fits console use case |
| Search/Filter | In-memory list comprehensions | Constitutional mandate, sufficient performance |
| Sorting | Display-layer concern | Separation of concerns |
| Due Dates | Inline indicators, no background process | Console-only constraint |
| Colors | colorama library | Cross-platform, constitutional allowance |
| Validation | Service layer with clear errors | Testable, maintainable |
| Menu | Add filter/search submenu | Keeps main menu simple |
| Testing | Unit for filters, integration for workflows | Matches complexity |

---

## Risk Analysis

### Risk 1: Date/Time Handling Complexity
- **Mitigation**: Use standard `datetime` library, no timezones (local time only)
- **Fallback**: If users need timezone support, defer to Phase-3

### Risk 2: Recurrence Logic Edge Cases
- **Mitigation**: Comprehensive test coverage for month/year boundaries
- **Examples**: Regenerate on Jan 31 → Feb 28/29, leap years

### Risk 3: Console Display Overflow
- **Mitigation**: Truncate long titles/descriptions in list view, full text in detail view
- **Example**: "This is a very long task title..." (max 50 chars in list)

---

**Research Complete**: All architectural unknowns resolved. Ready for Phase 1 design artifacts.
