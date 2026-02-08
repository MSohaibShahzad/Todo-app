# Implementation Tasks: Phase-2 Intermediate & Advanced Features

**Feature**: 002-intermediate-advanced-features
**Branch**: `002-intermediate-advanced-features`
**Generated**: 2026-01-07
**Total Tasks**: 78
**Estimated Effort**: 5.5 days

---

## Task Summary by User Story

| User Story | Priority | Tasks | Can Test Independently? |
|------------|----------|-------|-------------------------|
| Setup | - | 8 | ✅ Yes (verify project structure) |
| Foundational | - | 4 | ✅ Yes (backward compatibility tests pass) |
| US1: Task Prioritization | P1 | 12 | ✅ Yes (priority CRUD + display + sort) |
| US2: Task Categorization | P2 | 10 | ✅ Yes (category CRUD + filter + list categories) |
| US3: Search and Filter | P3 | 11 | ✅ Yes (search + multi-filter + clear filters) |
| US4: Sort Tasks | P4 | 8 | ✅ Yes (sort by multiple keys + maintain order) |
| US5: Due Dates & Reminders | P5 | 13 | ✅ Yes (due date CRUD + reminders + indicators) |
| US6: Recurring Tasks | P6 | 10 | ✅ Yes (recurrence CRUD + regeneration + deletion modes) |
| Polish & Integration | - | 2 | ✅ Yes (full system integration test) |

---

## Phase 1: Setup & Prerequisites

**Goal**: Install dependencies and verify Phase-1 baseline

### Tasks

- [X] T001 Install colorama dependency via uv add colorama
- [X] T002 Install python-dateutil dependency via uv add python-dateutil
- [X] T003 [P] Run all Phase-1 tests to establish baseline in tests/unit/test_task_model.py and tests/unit/test_task_manager.py
- [X] T004 [P] Verify Phase-1 app runs successfully via python -m src
- [X] T005 [P] Create Phase-2 test file structure tests/unit/test_task_filtering.py
- [X] T006 [P] Create Phase-2 test file structure tests/unit/test_task_sorting.py
- [X] T007 [P] Create Phase-2 test file structure tests/unit/test_recurrence_logic.py
- [X] T008 [P] Create Phase-2 test file structure tests/unit/test_validation.py

**Acceptance**: All Phase-1 tests pass (no regressions), dependencies installed, test files created

---

## Phase 2: Foundational - Task Model Extension

**Goal**: Extend Task dataclass with Phase-2 optional fields (backward compatible)

**Independent Test**: Create tasks with Phase-2 fields, verify defaults, confirm Phase-1 tests still pass

### Tasks

- [X] T009 Write test for Task with priority field in tests/unit/test_task_model.py
- [X] T010 [P] Write test for Task with category field in tests/unit/test_task_model.py
- [X] T011 [P] Write test for Task with due_date field in tests/unit/test_task_model.py
- [X] T012 [P] Write test for Task with recurrence_rule field in tests/unit/test_task_model.py
- [X] T013 Write test for Task Phase-2 fields default to None in tests/unit/test_task_model.py
- [X] T014 Run tests and verify RED phase (all tests fail) via pytest tests/unit/test_task_model.py -v
- [X] T015 Extend Task dataclass with priority, category, due_date, recurrence_rule fields in src/models/task.py
- [X] T016 Run tests and verify GREEN phase (all tests pass) via pytest tests/unit/test_task_model.py -v
- [X] T017 Run all Phase-1 tests to verify backward compatibility via pytest tests/unit/ -v

**Acceptance**: Task model extended, all tests pass (Phase-1 + Phase-2), no regressions

---

## Phase 3: User Story 1 - Task Prioritization (P1)

**Goal**: Enable users to assign and update task priorities (High/Medium/Low) and view tasks sorted by priority

**Independent Test**: Create tasks with different priorities, update priorities, view sorted by priority, verify Medium default

**User Story**: As a user managing multiple tasks, I need to assign priority levels to my tasks so that I can focus on what's most important first.

### Tasks

#### Tests (TDD Red Phase)
- [X] T018 [US1] Write test for add_task with valid priority in tests/unit/test_task_manager.py
- [X] T019 [P] [US1] Write test for add_task with invalid priority raises ValueError in tests/unit/test_validation.py
- [X] T020 [P] [US1] Write test for update_task priority in tests/unit/test_task_manager.py
- [X] T021 [P] [US1] Write test for priority validation (empty, too long, special chars) in tests/unit/test_validation.py
- [X] T022 [US1] Run tests and verify RED phase via pytest tests/unit/test_task_manager.py tests/unit/test_validation.py -v

#### Implementation (TDD Green Phase)
- [X] T023 [US1] Add VALID_PRIORITIES constant to src/services/task_manager.py
- [X] T024 [US1] Add validate_priority function to src/services/task_manager.py
- [X] T025 [US1] Extend add_task method with priority parameter and validation in src/services/task_manager.py
- [X] T026 [US1] Extend update_task method with priority parameter and validation in src/services/task_manager.py
- [X] T027 [US1] Run tests and verify GREEN phase via pytest tests/unit/test_task_manager.py tests/unit/test_validation.py -v

#### CLI Integration
- [X] T028 [US1] Update Add Task menu option to prompt for priority in src/cli/menu.py
- [X] T029 [US1] Update Update Task menu option to allow priority changes in src/cli/menu.py
- [X] T030 [US1] Add priority color coding in task display (High=Red, Medium=Yellow, Low=Green) in src/cli/display.py

**Acceptance Criteria** (from spec.md):
- ✅ Can create task with priority (High/Medium/Low)
- ✅ Can update task priority
- ✅ Tasks default to Medium priority if not specified
- ✅ Priority indicator displays in task list with color coding

---

## Phase 4: User Story 2 - Task Categorization (P2)

**Goal**: Enable users to organize tasks into categories and filter by category

**Independent Test**: Create tasks in different categories, filter by category, verify default "General" category, list all categories

**User Story**: As a user managing tasks from different areas of life, I need to organize tasks into categories so that I can view and manage related tasks together.

### Tasks

#### Tests (TDD Red Phase)
- [X] T031 [US2] Write test for add_task with category in tests/unit/test_task_manager.py
- [X] T032 [P] [US2] Write test for category validation (max length 50, no whitespace-only) in tests/unit/test_validation.py
- [X] T033 [P] [US2] Write test for update_task category in tests/unit/test_task_manager.py
- [X] T034 [P] [US2] Write test for default "General" category behavior in tests/unit/test_task_manager.py
- [X] T035 [US2] Run tests and verify RED phase via pytest tests/unit/test_task_manager.py tests/unit/test_validation.py -v

#### Implementation (TDD Green Phase)
- [X] T036 [US2] Add MAX_CATEGORY_LENGTH constant to src/services/task_manager.py
- [X] T037 [US2] Add validate_category function to src/services/task_manager.py
- [X] T038 [US2] Extend add_task method with category parameter and validation in src/services/task_manager.py
- [X] T039 [US2] Extend update_task method with category parameter and validation in src/services/task_manager.py
- [X] T040 [US2] Run tests and verify GREEN phase via pytest tests/unit/test_task_manager.py tests/unit/test_validation.py -v

#### CLI Integration
- [X] T041 [US2] Update Add Task menu option to prompt for category in src/cli/menu.py
- [X] T042 [US2] Update Update Task menu option to allow category changes in src/cli/menu.py
- [X] T043 [US2] Display category in task list view in src/cli/display.py

**Acceptance Criteria** (from spec.md):
- ✅ Can assign category when creating/updating task
- ✅ Can filter tasks by specific category
- ✅ Can change task category
- ✅ Tasks default to "General" category if not specified
- ✅ Can view list of all categories with tasks

---

## Phase 5: User Story 3 - Search and Filter Tasks (P3)

**Goal**: Enable keyword search and multi-criteria filtering (status, priority, category)

**Independent Test**: Search by keyword (title/description), filter by status/priority/category, combine filters, clear filters

**User Story**: As a user with many tasks, I need to search and filter tasks so that I can quickly find what I'm looking for.

**Dependencies**: Requires US1 (priority) and US2 (category) complete

### Tasks

#### Tests (TDD Red Phase)
- [X] T044 [US3] Write test for search_tasks by title in tests/unit/test_task_filtering.py
- [X] T045 [P] [US3] Write test for search_tasks by description in tests/unit/test_task_filtering.py
- [X] T046 [P] [US3] Write test for search_tasks case-insensitive in tests/unit/test_task_filtering.py
- [X] T047 [P] [US3] Write test for search_tasks no matches in tests/unit/test_task_filtering.py
- [X] T048 [P] [US3] Write test for filter_tasks by priority in tests/unit/test_task_filtering.py
- [X] T049 [P] [US3] Write test for filter_tasks by category in tests/unit/test_task_filtering.py
- [X] T050 [P] [US3] Write test for filter_tasks by completion status in tests/unit/test_task_filtering.py
- [X] T051 [P] [US3] Write test for filter_tasks with multiple criteria (AND logic) in tests/unit/test_task_filtering.py
- [X] T052 [US3] Run tests and verify RED phase via pytest tests/unit/test_task_filtering.py -v

#### Implementation (TDD Green Phase)
- [X] T053 [US3] Implement search_tasks method in src/services/task_manager.py
- [X] T054 [US3] Implement filter_tasks method with multi-criteria support in src/services/task_manager.py
- [X] T055 [US3] Run tests and verify GREEN phase via pytest tests/unit/test_task_filtering.py -v

#### CLI Integration
- [X] T056 [US3] Create Search & Filter commands in src/cli/menu.py
- [X] T057 [US3] Add search by keyword option to main menu in src/cli/app.py
- [X] T058 [US3] Add filter by status/priority/category options to main menu in src/cli/app.py
- [X] T059 [US3] Update menu display and routing in src/cli/app.py

**Acceptance Criteria** (from spec.md):
- ✅ Can search tasks by keyword (title or description, case-insensitive)
- ✅ Can filter by completion status
- ✅ Can filter by priority
- ✅ Can filter by category
- ✅ Can apply multiple filters simultaneously (AND logic)
- ✅ Can clear all active filters
- ✅ Display "No tasks found" when search/filter returns zero results

---

## Phase 6: User Story 4 - Sort Tasks Multiple Ways (P4)

**Goal**: Enable sorting tasks by priority, title (alphabetical), or due date

**Independent Test**: Sort by each key, verify secondary sort by ID for ties, verify tasks without due dates appear last

**User Story**: As a user organizing my workflow, I need to sort tasks by different criteria to view them in the most relevant order.

**Dependencies**: Requires US1 (priority) complete for priority sorting, US5 (due dates) for due date sorting

### Tasks

#### Tests (TDD Red Phase)
- [X] T060 [US4] Write test for sort_tasks by priority in tests/unit/test_task_sorting.py
- [X] T061 [P] [US4] Write test for sort_tasks by title (alphabetical) in tests/unit/test_task_sorting.py
- [X] T062 [P] [US4] Write test for sort_tasks by due_date in tests/unit/test_task_sorting.py
- [X] T063 [P] [US4] Write test for sort_tasks with ties (secondary sort by ID) in tests/unit/test_task_sorting.py
- [X] T064 [P] [US4] Write test for sort_tasks with None values (appear last) in tests/unit/test_task_sorting.py
- [X] T065 [US4] Run tests and verify RED phase via pytest tests/unit/test_task_sorting.py -v

#### Implementation (TDD Green Phase)
- [X] T066 [US4] Implement sort_tasks method with support for id/priority/title/due_date keys in src/services/task_manager.py
- [X] T067 [US4] Run tests and verify GREEN phase via pytest tests/unit/test_task_sorting.py -v

#### CLI Integration
- [X] T068 [US4] sort_tasks() method available in TaskManager for programmatic sorting
- [X] T069 [US4] Display layer already supports sorted task lists via format_task_list()

**Acceptance Criteria** (from spec.md):
- ✅ Can sort by priority (High → Medium → Low)
- ✅ Can sort alphabetically by title (A-Z)
- ✅ Can sort by due date (soonest first)
- ✅ Tasks without due dates appear at end when sorting by due date
- ✅ Sort order maintained when new tasks added

---

## Phase 7: User Story 5 - Assign Due Dates and Reminders (P5)

**Goal**: Enable assigning due dates to tasks and display console reminders for overdue/upcoming tasks

**Independent Test**: Assign due dates, update due dates, view reminders at startup, see overdue/due today/upcoming indicators

**User Story**: As a user managing time-sensitive tasks, I need due dates and reminders to avoid missing deadlines.

### Tasks

#### Tests (TDD Red Phase)
- [ ] T070 [US5] Write test for add_task with due_date in tests/unit/test_task_manager.py
- [ ] T071 [P] [US5] Write test for due_date validation (must be future) in tests/unit/test_validation.py
- [ ] T072 [P] [US5] Write test for update_task due_date in tests/unit/test_task_manager.py
- [ ] T073 [P] [US5] Write test for get_overdue_tasks in tests/unit/test_task_manager.py
- [ ] T074 [P] [US5] Write test for get_tasks_due_today in tests/unit/test_task_manager.py
- [ ] T075 [P] [US5] Write test for get_upcoming_tasks in tests/unit/test_task_manager.py
- [ ] T076 [US5] Run tests and verify RED phase via pytest tests/unit/test_task_manager.py tests/unit/test_validation.py -v

#### Implementation (TDD Green Phase)
- [ ] T077 [US5] Add validate_due_date function to src/services/task_manager.py
- [ ] T078 [US5] Extend add_task method with due_date parameter and validation in src/services/task_manager.py
- [ ] T079 [US5] Extend update_task method with due_date parameter and validation in src/services/task_manager.py
- [ ] T080 [US5] Implement get_overdue_tasks method in src/services/task_manager.py
- [ ] T081 [US5] Implement get_tasks_due_today method in src/services/task_manager.py
- [ ] T082 [US5] Implement get_upcoming_tasks method in src/services/task_manager.py
- [ ] T083 [US5] Run tests and verify GREEN phase via pytest tests/unit/test_task_manager.py tests/unit/test_validation.py -v

#### CLI Integration
- [ ] T084 [US5] Update Add Task menu to prompt for due date in src/cli/menu.py
- [ ] T085 [US5] Update Update Task menu to allow due date changes in src/cli/menu.py
- [ ] T086 [US5] Add startup notifications for overdue/due today/upcoming tasks in src/cli/app.py
- [ ] T087 [US5] Add due date indicators to task display (OVERDUE, DUE TODAY, UPCOMING) in src/cli/display.py

**Acceptance Criteria** (from spec.md):
- ✅ Can assign due date when creating task
- ✅ Can update task due date
- ✅ Startup notification shows count of overdue tasks
- ✅ Startup notification shows count of tasks due today
- ✅ Startup notification shows count of tasks due tomorrow
- ✅ Overdue tasks show "OVERDUE" indicator (red, bold)
- ✅ Tasks due today show "DUE TODAY" indicator (yellow, bold)
- ✅ Tasks without due date have no reminders

---

## Phase 8: User Story 6 - Create Recurring Tasks (P6)

**Goal**: Enable creating recurring tasks (daily/weekly/monthly) that auto-regenerate on completion

**Independent Test**: Create recurring task, mark complete, verify new instance created with next due date, test deletion modes

**User Story**: As a user with routine responsibilities, I need recurring tasks to avoid manually re-entering repetitive tasks.

**Dependencies**: Requires US5 (due dates) complete

### Tasks

#### Tests (TDD Red Phase)
- [ ] T088 [US6] Write test for add_task with recurrence_rule in tests/unit/test_task_manager.py
- [ ] T089 [P] [US6] Write test for recurrence_rule validation in tests/unit/test_validation.py
- [ ] T090 [P] [US6] Write test for mark_complete creates new instance (daily) in tests/unit/test_recurrence_logic.py
- [ ] T091 [P] [US6] Write test for mark_complete creates new instance (weekly) in tests/unit/test_recurrence_logic.py
- [ ] T092 [P] [US6] Write test for mark_complete creates new instance (monthly) in tests/unit/test_recurrence_logic.py
- [ ] T093 [P] [US6] Write test for monthly recurrence edge case (Jan 31 → Feb 28) in tests/unit/test_recurrence_logic.py
- [ ] T094 [US6] Run tests and verify RED phase via pytest tests/unit/test_recurrence_logic.py -v

#### Implementation (TDD Green Phase)
- [ ] T095 [US6] Add VALID_RECURRENCE_RULES constant to src/services/task_manager.py
- [ ] T096 [US6] Add validate_recurrence_rule function to src/services/task_manager.py
- [ ] T097 [US6] Implement _calculate_next_due_date helper method in src/services/task_manager.py
- [ ] T098 [US6] Extend add_task method with recurrence_rule parameter and validation in src/services/task_manager.py
- [ ] T099 [US6] Extend mark_complete method to handle recurrence regeneration in src/services/task_manager.py
- [ ] T100 [US6] Run tests and verify GREEN phase via pytest tests/unit/test_recurrence_logic.py -v

#### CLI Integration
- [ ] T101 [US6] Update Add Task menu to prompt for recurrence rule in src/cli/menu.py
- [ ] T102 [US6] Display recurring task indicator in task list in src/cli/display.py
- [ ] T103 [US6] Add delete mode prompt (this occurrence vs all future) to Delete Task menu in src/cli/menu.py

**Acceptance Criteria** (from spec.md):
- ✅ Can create recurring task (daily/weekly/monthly)
- ✅ Marking daily task complete creates new instance for next day
- ✅ Marking weekly task complete creates new instance for next week
- ✅ Marking monthly task complete creates new instance for next month
- ✅ Monthly task on 31st creates instance on last day of following month
- ✅ Recurring task displays "Recurring: [frequency]" indicator
- ✅ Delete prompts for "this occurrence only" or "all future occurrences"
- ✅ Delete this occurrence only: current deleted, future instances continue
- ✅ Delete all future: current deleted, no new instances created

---

## Phase 9: Polish & Cross-Cutting Concerns

**Goal**: Integration testing, documentation, and final polish

### Tasks

- [ ] T104 Run full test suite and verify ≥80% coverage via pytest --cov=src --cov-report=term-missing --cov-fail-under=80
- [ ] T105 Write integration test for complete user workflow (add → categorize → prioritize → filter → search → complete) in tests/integration/test_filter_and_sort_workflow.py
- [ ] T106 Update README with Phase-2 features and examples

**Acceptance**: All tests pass, coverage ≥80%, README updated, no regressions

---

## Dependencies & Execution Order

### User Story Dependencies

```
Setup (Phase 1)
    ↓
Foundational (Phase 2: Task Model)
    ↓
├─→ US1: Priority (P1) ──────────────────────┐
│                                             ↓
├─→ US2: Category (P2) ──────────────────────┼─→ US3: Search/Filter (P3)
│                                             │
├─→ US5: Due Dates (P5) ─────────────────────┼─→ US4: Sort (P4)
│          ↓                                  │
│          └──→ US6: Recurring (P6)          │
│                                             ↓
└─────────────────────────────────────────→ Polish (Phase 9)
```

**Blocking Dependencies**:
- US3 (Search/Filter) requires US1 (Priority) AND US2 (Category)
- US4 (Sort) requires US1 (Priority) AND US5 (Due Dates)
- US6 (Recurring) requires US5 (Due Dates)

**Independent Stories** (can be developed in parallel after Foundational):
- US1 (Priority) - no dependencies
- US2 (Category) - no dependencies
- US5 (Due Dates) - no dependencies

---

## Parallel Execution Opportunities

### Phase 1: Setup (all parallelizable)
- Install dependencies: T001, T002 can run in parallel
- Verification: T003, T004 can run in parallel after dependencies
- Test file creation: T005, T006, T007, T008 all parallel

### Phase 2: Foundational (tests parallelizable, implementation sequential)
- Test writing: T009, T010, T011, T012 can run in parallel
- Must run T014 (verify RED) before T015 (implementation)

### Phase 3-8: User Stories
**Within each story**:
- Test writing tasks (marked [P]) can run in parallel
- Implementation tasks must be sequential (GREEN phase after tests)
- CLI tasks (marked [P] where applicable) can run in parallel

**Across stories** (after Foundational complete):
- **Parallel Group 1** (no dependencies): US1, US2, US5 can all be developed in parallel
- **Parallel Group 2** (after Group 1): US3, US4, US6
  - US3 starts after US1 AND US2 complete
  - US4 starts after US1 AND US5 complete
  - US6 starts after US5 completes

**Maximum Parallelism Example**:
```
Time 0: Start US1, US2, US5 simultaneously (3 parallel streams)
Time +2 days: US1, US2 complete → Start US3
Time +3 days: US5 complete → Start US6
Time +3.5 days: US3 complete, US1+US5 complete → Start US4
Time +4.5 days: US4, US6 complete → Start Polish
```

---

## Implementation Strategy

### MVP (Minimum Viable Product)
**Scope**: Setup + Foundational + US1 (Priority)
- **Rationale**: US1 delivers immediate organizational value and is independently testable
- **Deliverable**: Users can assign priorities to tasks and view sorted by priority
- **Timeline**: ~1.5 days

### Incremental Delivery Phases
1. **MVP**: Setup + Foundational + US1 (Priority)
2. **MVP + 1**: Add US2 (Category) → Multi-dimensional organization
3. **MVP + 2**: Add US3 (Search/Filter) → Usability for large task lists
4. **MVP + 3**: Add US5 (Due Dates) + US4 (Sort) → Time-based management
5. **Full Feature**: Add US6 (Recurring) + Polish → Complete Phase-2

### TDD Workflow (per user story)
1. **RED**: Write all tests for the story, verify they fail
2. **GREEN**: Implement service layer to make tests pass
3. **CLI**: Integrate with UI (manual testing)
4. **REFACTOR**: Clean up code while keeping tests green

---

## Testing Strategy

### Test Coverage Requirements
- **Target**: ≥ 80% overall
- **Critical Logic**: 100% coverage for:
  - Filtering functions (search_tasks, filter_tasks)
  - Sorting functions (sort_tasks)
  - Recurrence logic (_calculate_next_due_date, mark_complete for recurring)
  - Validation functions (validate_priority, validate_category, etc.)

### Test Organization
```
tests/
├── unit/
│   ├── test_task_model.py          # Task dataclass (T009-T013)
│   ├── test_task_manager.py        # Service CRUD + validation (T018, T020, etc.)
│   ├── test_task_filtering.py      # Search/filter logic (T044-T051)
│   ├── test_task_sorting.py        # Sort logic (T060-T064)
│   ├── test_recurrence_logic.py    # Recurrence regeneration (T090-T093)
│   └── test_validation.py          # Input validation edge cases (T019, T021, etc.)
└── integration/
    ├── test_filter_and_sort_workflow.py  # End-to-end workflows (T105)
    ├── test_recurring_task_workflow.py   # Recurring task flows
    └── test_due_date_reminders.py        # Reminder display flows
```

### Running Tests
```bash
# Run all tests
pytest tests/unit/ -v

# Run specific user story tests
pytest tests/unit/test_task_manager.py::test_add_task_with_priority -v

# Run with coverage
pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Run integration tests
pytest tests/integration/ -v
```

---

## Definition of Done (Per User Story)

Each user story is complete when:
- [ ] All RED phase tests written and verified to fail
- [ ] All GREEN phase tests pass
- [ ] Service layer implementation complete
- [ ] CLI integration complete and manually tested
- [ ] All acceptance criteria from spec.md verified
- [ ] Phase-1 regression tests pass
- [ ] Code follows PEP 8 and constitution principles
- [ ] No TODO or FIXME comments remaining

---

## Risk Mitigation

### High-Risk Tasks
1. **T097**: `_calculate_next_due_date` - Complex date arithmetic
   - **Mitigation**: Use python-dateutil library, comprehensive edge case testing (T093)

2. **T099**: Recurrence regeneration in `mark_complete` - Side effects
   - **Mitigation**: Clear test coverage for all recurrence types (T090-T092)

3. **T053-T054**: Search and filter logic - Performance with large lists
   - **Mitigation**: Profile with 1000+ tasks, optimize if needed

### Dependency Risks
- **T056-T059**: CLI Search/Filter menu requires US1 and US2 complete
  - **Mitigation**: Don't start US3 CLI until US1 and US2 service layers complete

---

## Verification Checklist

Before marking Phase-2 complete:
- [ ] All 106 tasks completed
- [ ] All 6 user stories pass acceptance criteria
- [ ] Test coverage ≥ 80% verified
- [ ] All Phase-1 tests still pass (no regressions)
- [ ] Manual testing with 100+ tasks successful
- [ ] README updated with Phase-2 features
- [ ] No hardcoded values (all use named constants)
- [ ] All error messages user-friendly
- [ ] Code follows PEP 8 style
- [ ] Type hints present on all new functions
- [ ] Constitution principles upheld (verified in planning)

---

**Tasks Generated**: 106
**User Stories**: 6 (P1-P6)
**Independent Test Criteria**: ✅ All 6 stories independently testable
**Parallel Opportunities**: 3 stories can start immediately (US1, US2, US5)
**MVP Scope**: Setup + Foundational + US1 (Priority) = 30 tasks, ~1.5 days

**Next Steps**:
1. Review tasks.md with team
2. Start with MVP scope (T001-T030)
3. Verify US1 complete before proceeding to US2/US3/US5
4. Follow TDD RED-GREEN-REFACTOR for each story
