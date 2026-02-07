# CLI Interface Contract: Intermediate & Advanced Features

## Overview
This contract defines the console interface for interacting with the extended Todo app (Phase-2). All interactions are text-based, menu-driven, and executed in a terminal/console environment.

---

## 1. Main Menu

### Display Format
```
========================================
          TODO APP - MAIN MENU
========================================

1. Add Task
2. View All Tasks
3. Search & Filter Tasks
4. Update Task
5. Mark Complete/Incomplete
6. Delete Task
7. View Statistics
8. Exit

Enter your choice (1-8):
```

### Menu Options

#### Option 1: Add Task
Prompts for task details and creates a new task.

**User Flow**:
```
Enter task title: [user input]
Enter task description (optional, press Enter to skip): [user input]
Enter priority (low/medium/high, press Enter to skip): [user input]
Enter category (press Enter to skip): [user input]
Enter due date (YYYY-MM-DD HH:MM, press Enter to skip): [user input]
Is this a recurring task? (y/n): [user input]
  If yes: Enter recurrence (daily/weekly/monthly): [user input]

✓ Task added successfully! (ID: 5)
```

**Validation Messages**:
- `❌ Title cannot be empty`
- `❌ Title too long (max 200 characters)`
- `❌ Invalid priority. Choose from: low, medium, high`
- `❌ Category too long (max 50 characters)`
- `❌ Invalid date format. Use YYYY-MM-DD HH:MM`
- `❌ Due date must be in the future`
- `❌ Invalid recurrence. Choose from: daily, weekly, monthly`

---

#### Option 2: View All Tasks
Displays all tasks in a formatted list.

**Display Format (No Tasks)**:
```
========================================
              ALL TASKS
========================================

No tasks found. Start by adding a task!
```

**Display Format (With Tasks)**:
```
========================================
              ALL TASKS (5)
========================================

[1] ✓ Buy groceries                        [MEDIUM | Personal]
    Milk, eggs, bread
    Due: 2026-01-10 18:00

[2] ☐ Team standup                         [HIGH | Work] [RECURRING: daily]
    Daily sync with team
    Due: 2026-01-08 09:00 [DUE TODAY]

[3] ☐ Review PR #42                        [HIGH | Work]
    Security updates
    Due: 2026-01-05 17:00 [OVERDUE]

[4] ☐ Plan vacation                        [LOW | Personal]
    Research destinations
    Due: 2026-01-15 12:00 [UPCOMING]

[5] ☐ Write documentation                  [NONE | Work]
    API endpoints documentation

========================================
Legend:
✓ = Complete  |  ☐ = Incomplete
[OVERDUE] = Past due date
[DUE TODAY] = Due today
[UPCOMING] = Due within 3 days
========================================
```

**Color Coding** (using colorama):
- Priority HIGH: Red
- Priority MEDIUM: Yellow
- Priority LOW: Green
- Priority NONE: Default (white/gray)
- Completed tasks: Dim/gray
- [OVERDUE]: Red + Bold
- [DUE TODAY]: Yellow + Bold
- [UPCOMING]: Blue

---

#### Option 3: Search & Filter Tasks
Opens a submenu for searching and filtering.

**Submenu Display**:
```
========================================
        SEARCH & FILTER TASKS
========================================

1. Search by keyword
2. Filter by status (complete/incomplete)
3. Filter by priority
4. Filter by category
5. Sort results
6. Clear filters (show all)
7. Back to main menu

Enter your choice (1-7):
```

**Sub-option 3.1: Search by keyword**
```
Enter search keyword: meeting

Found 2 tasks matching "meeting":

[2] ☐ Team standup                         [HIGH | Work]
    Daily sync with team
    Due: 2026-01-08 09:00 [DUE TODAY]

[8] ☐ Prepare meeting notes               [MEDIUM | Work]
    Q1 planning meeting
    Due: 2026-01-12 14:00
```

**Sub-option 3.2: Filter by status**
```
Filter by status:
1. Show incomplete tasks only
2. Show complete tasks only
3. Show all tasks

Enter your choice (1-3): 1

Showing 4 incomplete tasks:
[Display tasks...]
```

**Sub-option 3.3: Filter by priority**
```
Filter by priority:
1. High
2. Medium
3. Low
4. No priority
5. Show all

Enter your choice (1-5): 1

Showing 2 high-priority tasks:
[Display tasks...]
```

**Sub-option 3.4: Filter by category**
```
Available categories:
- Work (3 tasks)
- Personal (2 tasks)

Enter category name (or press Enter for all): Work

Showing 3 tasks in "Work" category:
[Display tasks...]
```

**Sub-option 3.5: Sort results**
```
Sort by:
1. ID (creation order)
2. Priority (high to low)
3. Due date (earliest first)
4. Title (alphabetical)
5. Category (alphabetical)

Enter your choice (1-5): 2

Tasks sorted by priority:
[Display tasks with high priority first...]
```

---

#### Option 4: Update Task
Prompts for task ID and fields to update.

**User Flow**:
```
Enter task ID to update: 5

Current task details:
[5] ☐ Write documentation                  [NONE | Work]
    API endpoints documentation

What would you like to update?
1. Title
2. Description
3. Priority
4. Category
5. Due date
6. Recurrence rule
7. Cancel

Enter your choice (1-7): 3

Enter new priority (low/medium/high, or press Enter to remove): high

✓ Task updated successfully!

Updated task:
[5] ☐ Write documentation                  [HIGH | Work]
    API endpoints documentation
```

**Validation Messages**:
- `❌ Task not found: 5`
- `❌ Invalid priority. Choose from: low, medium, high`
- Same validation rules as Add Task

---

#### Option 5: Mark Complete/Incomplete
Toggles task completion status.

**User Flow (Non-Recurring)**:
```
Enter task ID to mark complete/incomplete: 1

[1] ✓ Buy groceries                        [MEDIUM | Personal]
    Milk, eggs, bread
    Current status: Complete

Mark as:
1. Complete
2. Incomplete

Enter your choice (1-2): 2

✓ Task marked as incomplete!
```

**User Flow (Recurring Task)**:
```
Enter task ID to mark complete: 2

[2] ☐ Team standup                         [HIGH | Work] [RECURRING: daily]
    Daily sync with team
    Due: 2026-01-08 09:00 [DUE TODAY]

Mark as complete? (y/n): y

✓ Task marked as complete!
✓ New recurring instance created (ID: 9)
  Next due date: 2026-01-09 09:00
```

---

#### Option 6: Delete Task
Deletes a task by ID (with confirmation).

**User Flow**:
```
Enter task ID to delete: 3

[3] ☐ Review PR #42                        [HIGH | Work]
    Security updates
    Due: 2026-01-05 17:00 [OVERDUE]

Are you sure you want to delete this task? (y/n): y

✓ Task deleted successfully!
```

**Cancellation**:
```
Are you sure you want to delete this task? (y/n): n

Deletion cancelled.
```

---

#### Option 7: View Statistics
Displays task statistics and summary.

**Display Format**:
```
========================================
          TASK STATISTICS
========================================

Total Tasks: 8
  ✓ Complete: 3 (37.5%)
  ☐ Incomplete: 5 (62.5%)

By Priority:
  High: 3 tasks
  Medium: 2 tasks
  Low: 1 task
  None: 2 tasks

By Category:
  Work: 5 tasks
  Personal: 3 tasks

Overdue Tasks: 1
Tasks Due Today: 1
Upcoming Tasks (3 days): 2
Recurring Tasks: 1

========================================
```

---

#### Option 8: Exit
Exits the application.

**Display**:
```
Thank you for using Todo App!
Goodbye!
```

---

## 2. Input Validation

### Date/Time Input
**Format**: `YYYY-MM-DD HH:MM`

**Examples**:
- Valid: `2026-01-15 14:30`
- Invalid: `01/15/2026`, `2026-1-15`, `15-01-2026 14:30`

**Validation**:
- Must match format exactly
- Month: 01-12
- Day: 01-31 (month-appropriate)
- Hour: 00-23
- Minute: 00-59
- Must be in the future

### Priority Input
**Valid**: `low`, `medium`, `high`, `` (empty = None)
**Invalid**: `Low`, `MEDIUM`, `urgent`, `1`, `2`, `3`
**Case**: Case-sensitive lowercase only

### Recurrence Input
**Valid**: `daily`, `weekly`, `monthly`, `` (empty = None)
**Invalid**: `Daily`, `WEEKLY`, `day`, `week`, `month`

### Category Input
**Valid**: Alphanumeric, spaces, hyphens, underscores
**Examples**:
- Valid: `Work`, `Personal Projects`, `Home_Tasks`, `Q1-Planning`
- Invalid: `Work!`, `@Home`, `#Personal`, `Task/Project`

---

## 3. Error Handling

### User-Friendly Error Messages
All errors display in a consistent format:
```
❌ [Error Type]: [Clear description]

Press Enter to continue...
```

**Examples**:
- `❌ Invalid Input: Title cannot be empty`
- `❌ Not Found: Task ID 99 does not exist`
- `❌ Validation Error: Due date must be in the future`
- `❌ Format Error: Date must be in format YYYY-MM-DD HH:MM`

### Input Retry
After an error, the user is prompted to try again (not kicked back to main menu):
```
Enter task title: [empty]
❌ Title cannot be empty

Enter task title: [user retries]
```

---

## 4. Color Scheme (via colorama)

### Priority Colors
- **High**: `Fore.RED + Style.BRIGHT`
- **Medium**: `Fore.YELLOW`
- **Low**: `Fore.GREEN`
- **None**: `Fore.WHITE` (default)

### Status Colors
- **Complete (✓)**: `Fore.WHITE + Style.DIM`
- **Incomplete (☐)**: `Fore.WHITE + Style.NORMAL`

### Alert Colors
- **[OVERDUE]**: `Fore.RED + Style.BRIGHT`
- **[DUE TODAY]**: `Fore.YELLOW + Style.BRIGHT`
- **[UPCOMING]**: `Fore.CYAN`

### Success/Error Messages
- **Success (✓)**: `Fore.GREEN`
- **Error (❌)**: `Fore.RED`

---

## 5. Accessibility Considerations

### Screen Reader Support
- Use ASCII symbols (✓, ☐, ❌) that are screen-reader friendly
- Avoid Unicode box-drawing characters
- Provide text alternatives: `[OVERDUE]` instead of `⚠️`

### Keyboard-Only Navigation
- All interactions via numbered menu choices
- No mouse required
- Clear instructions for each prompt

### Readable Output
- Consistent spacing and alignment
- Maximum line width: 80 characters (terminal-friendly)
- Clear visual hierarchy with separators

---

## 6. Performance Expectations

### Response Time
- Menu display: Instant (<10ms)
- Task list display (100 tasks): <100ms
- Search/filter (1000 tasks): <500ms
- Task creation/update/delete: Instant (<10ms)

### Screen Refresh
- Clear screen before displaying new menu (platform-agnostic via `os.system('clear')` or `os.system('cls')`)
- Redraw full menu after each operation

---

## 7. Backward Compatibility

### Phase-1 Menu Flow
All Phase-1 operations remain accessible:
- Add task (with optional new fields)
- View all tasks (with enhanced display)
- Update task (with optional new fields)
- Mark complete/incomplete (with recurring task support)
- Delete task (unchanged)

### Graceful Degradation
If colorama is not installed:
- Fall back to plain text (no colors)
- All functionality remains intact
- Display warning: `Note: Install 'colorama' for colored output`

---

**CLI Contract Complete**: All user interactions, inputs, outputs, and error handling defined.
