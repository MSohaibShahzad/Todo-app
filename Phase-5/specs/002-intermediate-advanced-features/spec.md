# Feature Specification: Phase II  Intermediate & Advanced Features

**Feature Branch**: `002-intermediate-advanced-features`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description: "Phase II  Todo Console App (Intermediate & Advanced Features). Extend the existing in-memory Todo console application with organizational and intelligent features while keeping the application console-based and simple."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task Prioritization (Priority: P1)

As a user managing multiple tasks, I need to assign priority levels to my tasks so that I can focus on what's most important first. I should be able to set a task as High, Medium, or Low priority and view tasks organized by priority.

**Why this priority**: Priority management is the foundation of effective task organization. Without it, users cannot distinguish urgent tasks from less critical ones. This is the most fundamental organizational feature that delivers immediate value.

**Independent Test**: Can be fully tested by creating tasks with different priority levels, updating priorities, and viewing the prioritized task list. Delivers immediate value by helping users focus on high-priority work.

**Acceptance Scenarios**:

1. **Given** I am adding a new task, **When** I specify a priority level (High, Medium, or Low), **Then** the task is created with that priority and displays a priority indicator
2. **Given** I have an existing task, **When** I update its priority from Low to High, **Then** the task's priority indicator changes accordingly
3. **Given** I have multiple tasks with different priorities, **When** I view my task list sorted by priority, **Then** High priority tasks appear first, followed by Medium, then Low
4. **Given** I add a task without specifying priority, **When** the task is created, **Then** it defaults to Medium priority

---

### User Story 2 - Task Categorization (Priority: P2)

As a user managing tasks from different areas of life, I need to organize tasks into categories (e.g., Work, Home, Personal, Shopping) so that I can view and manage related tasks together.

**Why this priority**: Categories provide essential context and organization, enabling users to separate work from personal tasks and focus on specific life areas. This builds on priority management to provide multi-dimensional organization.

**Independent Test**: Can be tested by creating categories, assigning tasks to categories, and filtering tasks by category. Delivers value by enabling context switching between different life areas.

**Acceptance Scenarios**:

1. **Given** I am adding a new task, **When** I assign it to a category (e.g., "Work"), **Then** the task is associated with that category
2. **Given** I have tasks in multiple categories, **When** I filter by a specific category, **Then** only tasks from that category are displayed
3. **Given** I have an existing task, **When** I change its category from "Work" to "Home", **Then** the task's category updates and appears in the Home filter
4. **Given** I create a task without specifying a category, **When** the task is created, **Then** it is assigned to a default "General" category
5. **Given** I want to view all available categories, **When** I request a category list, **Then** all categories that contain at least one task are displayed

---

### User Story 3 - Search and Filter Tasks (Priority: P3)

As a user with many tasks, I need to search for specific tasks by keyword and filter by status, priority, or category so that I can quickly find what I'm looking for without scrolling through long lists.

**Why this priority**: Search and filtering become essential as the task list grows. This enhances usability by providing multiple ways to locate tasks quickly. It depends on priority and category features being in place.

**Independent Test**: Can be tested by creating diverse tasks and verifying that search returns correct matches, and filters work independently and in combination. Delivers value by reducing time to find specific tasks.

**Acceptance Scenarios**:

1. **Given** I have tasks with various titles and descriptions, **When** I search for a keyword (e.g., "meeting"), **Then** all tasks containing "meeting" in title or description are displayed
2. **Given** I have completed and incomplete tasks, **When** I filter by completion status "incomplete", **Then** only incomplete tasks are shown
3. **Given** I have tasks with different priorities, **When** I filter by "High priority", **Then** only high-priority tasks are displayed
4. **Given** I have applied a category filter, **When** I add a priority filter on top, **Then** only tasks matching both filters are shown
5. **Given** I am viewing filtered results, **When** I clear all filters, **Then** the full task list is restored
6. **Given** I search with a keyword that matches no tasks, **When** the search completes, **Then** a message indicates "No tasks found matching your search"

---

### User Story 4 - Sort Tasks Multiple Ways (Priority: P4)

As a user organizing my workflow, I need to sort my tasks by priority, alphabetical order, or due date so that I can view tasks in the order most relevant to my current needs.

**Why this priority**: Sorting provides flexible task organization based on user preference and context. While useful, it's less critical than filtering because users can manually scan sorted lists. It builds on the foundation of priorities and due dates.

**Independent Test**: Can be tested by creating tasks with different attributes and verifying sort order changes correctly. Delivers value by adapting the view to different work styles.

**Acceptance Scenarios**:

1. **Given** I have tasks with different priorities, **When** I sort by priority, **Then** tasks are ordered High � Medium � Low
2. **Given** I have tasks with different titles, **When** I sort alphabetically, **Then** tasks are ordered A-Z by title
3. **Given** I have tasks with due dates, **When** I sort by due date, **Then** tasks are ordered from soonest to latest due date
4. **Given** some tasks have no due date, **When** I sort by due date, **Then** tasks with due dates appear first, followed by tasks without due dates
5. **Given** I have applied a sort order, **When** I add a new task, **Then** the task list re-sorts to maintain the selected order

---

### User Story 5 - Assign Due Dates and Reminders (Priority: P5)

As a user managing time-sensitive tasks, I need to assign due dates to tasks and receive console notifications when tasks are due soon or overdue so that I don't miss important deadlines.

**Why this priority**: Due dates add temporal context to tasks, making the system more useful for deadline-driven work. Reminders ensure users stay aware of upcoming deadlines. This is an advanced feature that significantly increases complexity.

**Independent Test**: Can be tested by creating tasks with various due dates (past, present, future) and verifying that reminders display appropriately when the app starts. Delivers value by preventing missed deadlines.

**Acceptance Scenarios**:

1. **Given** I am adding a task, **When** I assign a due date to it, **Then** the task stores the due date and displays it in the task list
2. **Given** I have a task with a due date, **When** I update the due date to a new value, **Then** the task's due date changes accordingly
3. **Given** the current date is 2026-01-06 and I have a task due on 2026-01-05, **When** I start the application, **Then** a console notification shows "You have 1 overdue task"
4. **Given** the current date is 2026-01-06 and I have a task due on 2026-01-07, **When** I start the application, **Then** a console notification shows "You have 1 task due tomorrow"
5. **Given** I have a task due today, **When** I view the task list, **Then** the task is highlighted with a "DUE TODAY" indicator
6. **Given** I have an overdue task, **When** I view the task list, **Then** the task is highlighted with an "OVERDUE" indicator
7. **Given** I create a task without specifying a due date, **When** the task is created, **Then** it has no due date and no deadline reminders apply

---

### User Story 6 - Create Recurring Tasks (Priority: P6)

As a user with routine responsibilities, I need to create recurring tasks (daily, weekly, monthly) so that I don't have to manually re-enter repetitive tasks.

**Why this priority**: Recurring tasks automate the creation of routine tasks, reducing manual work for users with regular responsibilities. This is the most complex feature and depends on due date functionality. It's lowest priority because it's a convenience feature that doesn't affect one-time task management.

**Independent Test**: Can be tested by creating a recurring task, marking it complete, and verifying that a new instance is automatically created with the next due date. Delivers value by automating routine task creation.

**Acceptance Scenarios**:

1. **Given** I am creating a task, **When** I set it to recur daily, **Then** the task is marked as recurring with a daily frequency
2. **Given** I have a daily recurring task due today, **When** I mark it complete, **Then** a new instance of the task is created with tomorrow's date
3. **Given** I have a weekly recurring task due on Monday, **When** I mark it complete on Monday, **Then** a new instance is created with next Monday's due date
4. **Given** I have a monthly recurring task due on the 1st, **When** I mark it complete, **Then** a new instance is created with the 1st of next month
5. **Given** I have a recurring task, **When** I view its details, **Then** it displays a "Recurring: [frequency]" indicator
6. **Given** I want to delete a recurring task, **When** I initiate deletion, **Then** the system prompts me to choose between "Delete this occurrence only" or "Delete all future occurrences"
7. **Given** I choose "Delete this occurrence only", **When** the deletion completes, **Then** only the current task is deleted and new instances continue to be created on schedule
8. **Given** I choose "Delete all future occurrences", **When** the deletion completes, **Then** the current task is deleted and no new instances are ever created

---

### Edge Cases

- **Empty categories**: What happens when a user filters by a category that has no tasks? Display "No tasks in this category"
- **Invalid priority values**: How does the system handle attempts to set priority to values other than High/Medium/Low? Reject with error message "Priority must be High, Medium, or Low"
- **Search with special characters**: How does search handle special characters or very long search strings? Treat special characters as literal text; limit search strings to 200 characters
- **Overdue task accumulation**: What happens when a user has many overdue tasks? Display count in startup notification; highlight overdue tasks in list view
- **Recurring task edge case**: What happens when a monthly recurring task is created on the 31st of a month? Create next instance on the last day of the following month (e.g., Jan 31 � Feb 28/29)
- **Due date in the past**: Can users set a due date in the past when creating a task? Yes, to accommodate backdated task entry; mark immediately as overdue
- **Multiple filters conflict**: What happens when filters produce an empty result set? Display "No tasks match your current filters" with option to clear filters
- **Sorting with ties**: When sorting by priority, how are tasks with the same priority ordered? Secondary sort by creation order (ID)

## Requirements *(mandatory)*

### Functional Requirements

**Priority Management**:
- **FR-001**: System MUST allow users to assign a priority level (High, Medium, Low) when creating a task
- **FR-002**: System MUST allow users to update the priority of an existing task
- **FR-003**: System MUST default new tasks to Medium priority if no priority is specified
- **FR-004**: System MUST display a visual indicator for each priority level in the task list

**Category Management**:
- **FR-005**: System MUST allow users to assign a category to a task when creating or updating it
- **FR-006**: System MUST provide a default "General" category for tasks without a specified category
- **FR-007**: System MUST display all categories that contain at least one task
- **FR-008**: System MUST allow users to view tasks from a single category

**Search Functionality**:
- **FR-009**: System MUST allow users to search for tasks by keyword in both title and description fields
- **FR-010**: System MUST perform case-insensitive searches
- **FR-011**: System MUST display all tasks containing the search keyword
- **FR-012**: System MUST display a "No tasks found" message when search returns zero results

**Filtering Functionality**:
- **FR-013**: System MUST allow users to filter tasks by completion status (complete/incomplete)
- **FR-014**: System MUST allow users to filter tasks by priority level
- **FR-015**: System MUST allow users to filter tasks by category
- **FR-016**: System MUST support applying multiple filters simultaneously (e.g., "High priority AND Work category")
- **FR-017**: System MUST allow users to clear all active filters

**Sorting Functionality**:
- **FR-018**: System MUST allow users to sort tasks by priority (High � Medium � Low)
- **FR-019**: System MUST allow users to sort tasks alphabetically by title (A-Z)
- **FR-020**: System MUST allow users to sort tasks by due date (soonest first)
- **FR-021**: System MUST place tasks without due dates at the end when sorting by due date
- **FR-022**: System MUST maintain sort order when new tasks are added

**Due Date Management**:
- **FR-023**: System MUST allow users to assign an optional due date to tasks
- **FR-024**: System MUST allow users to update or remove due dates from existing tasks
- **FR-025**: System MUST accept due dates in the past (for backdating)
- **FR-026**: System MUST display due dates in a consistent format (YYYY-MM-DD)
- **FR-027**: System MUST identify tasks as "overdue" when current date is past the due date
- **FR-028**: System MUST identify tasks as "due today" when due date matches current date
- **FR-029**: System MUST identify tasks as "due tomorrow" when due date is one day in the future

**Reminder/Notification System**:
- **FR-030**: System MUST display a console notification at startup showing count of overdue tasks (if any)
- **FR-031**: System MUST display a console notification at startup showing count of tasks due today (if any)
- **FR-032**: System MUST display a console notification at startup showing count of tasks due tomorrow (if any)
- **FR-033**: System MUST highlight overdue tasks with an "OVERDUE" indicator in the task list
- **FR-034**: System MUST highlight tasks due today with a "DUE TODAY" indicator in the task list

**Recurring Tasks**:
- **FR-035**: System MUST allow users to create recurring tasks with frequency options: Daily, Weekly, Monthly
- **FR-036**: System MUST automatically create a new instance of a recurring task when the current instance is marked complete
- **FR-037**: System MUST set the new instance's due date based on recurrence frequency:
  - Daily: next day
  - Weekly: same day next week
  - Monthly: same day next month (or last day if original day doesn't exist)
- **FR-038**: System MUST display a "Recurring: [frequency]" indicator for recurring tasks
- **FR-039**: System MUST prevent recurring tasks from generating instances more than one period in advance
- **FR-040**: System MUST prompt users when deleting a recurring task to choose between "Delete this occurrence only" or "Delete all future occurrences"
- **FR-041**: System MUST only delete the current instance if user chooses "Delete this occurrence only"
- **FR-042**: System MUST delete the current instance and stop all future instances if user chooses "Delete all future occurrences"

**Data Integrity**:
- **FR-043**: All existing Phase-1 features (add, view, update, delete, mark complete/incomplete) MUST continue to function unchanged
- **FR-044**: System MUST remain fully in-memory with no file or database persistence
- **FR-045**: System MUST validate all user inputs for priority, category, and due date fields

### Key Entities

- **Task** (extended from Phase-1): Represents a single task item with the following attributes:
  - ID (unique identifier, from Phase-1)
  - Title (text summary, from Phase-1)
  - Description (detailed text, from Phase-1)
  - Completion status (boolean, from Phase-1)
  - **Priority** (High/Medium/Low, new)
  - **Category** (text label, new)
  - **Due date** (optional date, new)
  - **Recurrence frequency** (none/Daily/Weekly/Monthly, new)

- **Category**: Represents a grouping label for tasks (lightweight entity)
  - Name (text label)
  - No separate storage needed; derived from tasks

- **Filter State**: Represents the current active filters (ephemeral, not persisted)
  - Status filter (complete/incomplete/all)
  - Priority filter (High/Medium/Low/all)
  - Category filter (specific category/all)
  - Search query (text string)

- **Sort Order**: Represents the current sort preference (ephemeral, not persisted)
  - Sort field (priority/alphabetical/due date)
  - Direction (ascending/descending where applicable)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can assign and update task priorities in under 5 seconds per task
- **SC-002**: Users can filter a list of 100 tasks by category in under 2 seconds
- **SC-003**: Search returns results instantaneously (under 1 second) for lists up to 1000 tasks
- **SC-004**: Users can create a recurring task and verify new instance generation in under 30 seconds
- **SC-005**: 100% of overdue and due-soon tasks are correctly identified and highlighted at startup
- **SC-006**: Users can switch between different sort orders (priority/alphabetical/due date) in under 3 seconds
- **SC-007**: All Phase-1 features continue to work without modification or regression
- **SC-008**: Users receive clear console notifications for overdue and upcoming tasks without needing to navigate menus
- **SC-009**: Task list remains readable and organized even with 50+ tasks across multiple categories and priorities
- **SC-010**: Users successfully complete multi-step workflows (create � categorize � prioritize � set due date � filter � search) in under 2 minutes

## Assumptions

- Users will primarily interact with the application through numbered menu choices and text input prompts
- Due dates will be entered in YYYY-MM-DD format or via a simple input helper
- Category names are user-defined and not pre-configured
- The console supports basic text formatting for visual indicators (symbols, spacing)
- Users will run the application frequently enough that startup notifications are useful for deadline awareness
- Monthly recurring tasks use calendar months, not 30-day intervals
- The system clock is accurate for due date calculations
