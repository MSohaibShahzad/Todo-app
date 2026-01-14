# Tasks: Todo In-Memory Python Console App

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED per Constitution Principle III (Test-Driven Development). All tasks follow Red-Green-Refactor cycle.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Initialize uv project with Python 3.13+ in repository root
- [ ] T002 Add pytest as dev dependency using uv add --dev pytest
- [ ] T003 [P] Create src directory structure: src/models/, src/services/, src/cli/
- [ ] T004 [P] Create tests directory structure: tests/unit/, tests/integration/
- [ ] T005 [P] Create __init__.py files in src/, src/models/, src/services/, src/cli/
- [ ] T006 [P] Create __init__.py files in tests/, tests/unit/, tests/integration/
- [ ] T007 Configure pytest in pyproject.toml with testpaths and python_files settings
- [ ] T008 [P] Create README.md with project overview and setup instructions
- [ ] T009 [P] Create .gitignore for Python (__pycache__/, .pytest_cache/, *.pyc, venv/)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T010 [P] Create Task dataclass in src/models/task.py with id, title, description, is_complete attributes
- [ ] T011 [P] Create TaskManager skeleton class in src/services/task_manager.py with __init__ method
- [ ] T012 [P] Define MAX_TITLE_LENGTH=200 and MAX_DESCRIPTION_LENGTH=1000 constants in src/services/task_manager.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks with title/description and view them in a list with status indicators

**Independent Test**: Launch app, add tasks, view list - confirm tasks appear with correct ID, title, description, and incomplete status

### Tests for User Story 1 (Red Phase - MUST FAIL before implementation)

- [ ] T013 [P] [US1] Write unit test for Task dataclass creation in tests/unit/test_task_model.py
- [ ] T014 [P] [US1] Write unit test for add_task() with sequential ID assignment in tests/unit/test_task_manager.py
- [ ] T015 [P] [US1] Write unit test for add_task() validation (empty title, title too long, description too long) in tests/unit/test_task_manager.py
- [ ] T016 [P] [US1] Write unit test for get_all_tasks() returning empty list in tests/unit/test_task_manager.py
- [ ] T017 [P] [US1] Write unit test for get_all_tasks() returning tasks sorted by ID in tests/unit/test_task_manager.py
- [ ] T018 [P] [US1] Write integration test for add and view workflow in tests/integration/test_workflows.py
- [ ] T019 [US1] Run pytest to verify all User Story 1 tests FAIL (Red phase confirmation)

### Implementation for User Story 1 (Green Phase)

- [ ] T020 [US1] Implement Task dataclass with proper type hints and defaults in src/models/task.py
- [ ] T021 [US1] Implement TaskManager.__init__ with tasks dict and next_id counter in src/services/task_manager.py
- [ ] T022 [US1] Implement TaskManager.add_task() with validation and ID assignment in src/services/task_manager.py
- [ ] T023 [US1] Implement TaskManager.get_all_tasks() returning sorted task list in src/services/task_manager.py
- [ ] T024 [US1] Run pytest to verify all User Story 1 unit tests PASS (Green phase for models/services)
- [ ] T025 [P] [US1] Create input validation helper get_string_input() in src/cli/menu.py
- [ ] T026 [P] [US1] Create display helper format_task_list() in src/cli/display.py
- [ ] T027 [P] [US1] Create display helper format_status_indicator() in src/cli/display.py
- [ ] T028 [US1] Implement add_task_command() function in src/cli/menu.py
- [ ] T029 [US1] Implement view_tasks_command() function in src/cli/menu.py
- [ ] T030 [US1] Create main() function with menu loop (options 1, 2, 7 only) in src/cli/app.py
- [ ] T031 [US1] Run pytest to verify all User Story 1 integration tests PASS (Green phase complete)

### Refactor Phase for User Story 1

- [ ] T032 [US1] Refactor: Extract common validation logic if duplicated, improve naming if needed
- [ ] T033 [US1] Refactor: Ensure PEP 8 compliance and type hints on all functions
- [ ] T034 [US1] Run pytest to confirm tests still PASS after refactoring

**Checkpoint**: At this point, User Story 1 (MVP) should be fully functional and testable independently. Users can add and view tasks.

---

## Phase 4: User Story 2 - Mark Tasks Complete or Incomplete (Priority: P2)

**Goal**: Users can toggle task status between complete and incomplete, with clear visual distinction in the list

**Independent Test**: Add tasks (P1), mark some complete, view list - confirm status changes are reflected with visual indicators (☐/☑)

### Tests for User Story 2 (Red Phase - MUST FAIL before implementation)

- [ ] T035 [P] [US2] Write unit test for mark_complete() changing status to True in tests/unit/test_task_manager.py
- [ ] T036 [P] [US2] Write unit test for mark_complete() changing status to False in tests/unit/test_task_manager.py
- [ ] T037 [P] [US2] Write unit test for mark_complete() with non-existent ID raising ValueError in tests/unit/test_task_manager.py
- [ ] T038 [P] [US2] Write unit test for mark_complete() idempotency (mark complete twice) in tests/unit/test_task_manager.py
- [ ] T039 [P] [US2] Write integration test for mark complete workflow in tests/integration/test_workflows.py
- [ ] T040 [US2] Run pytest to verify all User Story 2 tests FAIL (Red phase confirmation)

### Implementation for User Story 2 (Green Phase)

- [ ] T041 [US2] Implement TaskManager.mark_complete() with task_id and is_complete parameters in src/services/task_manager.py
- [ ] T042 [US2] Add ValueError handling for non-existent task ID in mark_complete() in src/services/task_manager.py
- [ ] T043 [US2] Run pytest to verify all User Story 2 unit tests PASS (Green phase for services)
- [ ] T044 [US2] Implement mark_complete_command() function in src/cli/menu.py
- [ ] T045 [US2] Implement mark_incomplete_command() function in src/cli/menu.py
- [ ] T046 [US2] Add menu options 5 and 6 to main menu in src/cli/app.py
- [ ] T047 [US2] Run pytest to verify all User Story 2 integration tests PASS (Green phase complete)

### Refactor Phase for User Story 2

- [ ] T048 [US2] Refactor: Extract error message constants if duplicated
- [ ] T049 [US2] Run pytest to confirm tests still PASS after refactoring

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can add, view, and mark tasks complete/incomplete.

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can edit task title or description, with partial updates supported (title-only or description-only)

**Independent Test**: Add task (P1), update title or description, view list - confirm changes are reflected while other fields remain unchanged

### Tests for User Story 3 (Red Phase - MUST FAIL before implementation)

- [ ] T050 [P] [US3] Write unit test for update_task() updating title only in tests/unit/test_task_manager.py
- [ ] T051 [P] [US3] Write unit test for update_task() updating description only in tests/unit/test_task_manager.py
- [ ] T052 [P] [US3] Write unit test for update_task() updating both title and description in tests/unit/test_task_manager.py
- [ ] T053 [P] [US3] Write unit test for update_task() with non-existent ID raising ValueError in tests/unit/test_task_manager.py
- [ ] T054 [P] [US3] Write unit test for update_task() validation (empty title, length limits) in tests/unit/test_task_manager.py
- [ ] T055 [P] [US3] Write integration test for update workflow in tests/integration/test_workflows.py
- [ ] T056 [US3] Run pytest to verify all User Story 3 tests FAIL (Red phase confirmation)

### Implementation for User Story 3 (Green Phase)

- [ ] T057 [US3] Implement TaskManager.update_task() with optional title and description parameters in src/services/task_manager.py
- [ ] T058 [US3] Add validation logic for partial updates in update_task() in src/services/task_manager.py
- [ ] T059 [US3] Add ValueError handling for non-existent task ID and validation failures in update_task() in src/services/task_manager.py
- [ ] T060 [US3] Run pytest to verify all User Story 3 unit tests PASS (Green phase for services)
- [ ] T061 [US3] Implement update_task_command() function with prompts for title and description in src/cli/menu.py
- [ ] T062 [US3] Add menu option 3 to main menu in src/cli/app.py
- [ ] T063 [US3] Run pytest to verify all User Story 3 integration tests PASS (Green phase complete)

### Refactor Phase for User Story 3

- [ ] T064 [US3] Refactor: Simplify validation logic if complex, extract helper if needed
- [ ] T065 [US3] Run pytest to confirm tests still PASS after refactoring

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently. Users have full add, view, mark, and update capabilities.

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can delete tasks by ID, keeping the task list clean and focused

**Independent Test**: Add tasks (P1), delete specific tasks by ID, view list - confirm only deleted tasks are removed, others remain

### Tests for User Story 4 (Red Phase - MUST FAIL before implementation)

- [ ] T066 [P] [US4] Write unit test for delete_task() returning True for existing ID in tests/unit/test_task_manager.py
- [ ] T067 [P] [US4] Write unit test for delete_task() returning False for non-existent ID in tests/unit/test_task_manager.py
- [ ] T068 [P] [US4] Write unit test for delete_task() removing task from get_all_tasks() in tests/unit/test_task_manager.py
- [ ] T069 [P] [US4] Write unit test for delete_task() not affecting other tasks in tests/unit/test_task_manager.py
- [ ] T070 [P] [US4] Write integration test for delete workflow in tests/integration/test_workflows.py
- [ ] T071 [US4] Run pytest to verify all User Story 4 tests FAIL (Red phase confirmation)

### Implementation for User Story 4 (Green Phase)

- [ ] T072 [US4] Implement TaskManager.delete_task() with task_id parameter in src/services/task_manager.py
- [ ] T073 [US4] Add logic to remove task from internal dict and return boolean in delete_task() in src/services/task_manager.py
- [ ] T074 [US4] Run pytest to verify all User Story 4 unit tests PASS (Green phase for services)
- [ ] T075 [P] [US4] Create input validation helper get_integer_input() in src/cli/menu.py
- [ ] T076 [US4] Implement delete_task_command() function in src/cli/menu.py
- [ ] T077 [US4] Add menu option 4 to main menu in src/cli/app.py
- [ ] T078 [US4] Run pytest to verify all User Story 4 integration tests PASS (Green phase complete)

### Refactor Phase for User Story 4

- [ ] T079 [US4] Refactor: Review all CLI command functions for consistency and DRY principle
- [ ] T080 [US4] Run pytest to confirm tests still PASS after refactoring

**Checkpoint**: All user stories (P1-P4) should now be independently functional. Full CRUD operations available.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and overall application quality

- [ ] T081 [P] Add comprehensive docstrings to all TaskManager methods in src/services/task_manager.py
- [ ] T082 [P] Add docstrings to all CLI helper functions in src/cli/menu.py and src/cli/display.py
- [ ] T083 [P] Verify all functions have type hints (check with mypy or manual review)
- [ ] T084 [P] Run PEP 8 compliance check (can use ruff check or black --check)
- [ ] T085 [P] Add edge case tests for very long titles/descriptions (1000+ chars) in tests/unit/test_task_manager.py
- [ ] T086 [P] Add edge case tests for non-numeric task ID input in tests/integration/test_workflows.py
- [ ] T087 [P] Test empty task list display message in tests/integration/test_workflows.py
- [ ] T088 Manually test full application workflow following quickstart.md guide
- [ ] T089 Verify application startup time is under 1 second (SC-009)
- [ ] T090 Verify task list with 100 tasks displays clearly (SC-002)
- [ ] T091 [P] Update README.md with final usage instructions and examples
- [ ] T092 Run complete test suite with pytest -v to confirm all tests pass

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent (uses P1 for integration tests but doesn't modify P1 code)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent (uses P1 for integration tests but doesn't modify P1 code)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent (uses P1 for integration tests but doesn't modify P1 code)

### Within Each User Story (TDD Workflow)

1. **Red Phase**: Write tests FIRST (T013-T019 for US1, etc.)
2. **Verify FAIL**: Run pytest to confirm tests fail before implementation (T019, T040, T056, T071)
3. **Green Phase**: Implement minimum code to pass tests (T020-T031 for US1, etc.)
4. **Verify PASS**: Run pytest to confirm tests pass (T024, T031, etc.)
5. **Refactor Phase**: Improve code while keeping tests green (T032-T034 for US1, etc.)
6. Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T003-T006, T008-T009 can run in parallel (different files)
- **Phase 2 (Foundational)**: T010-T012 can run in parallel (different files)
- **Within User Stories**:
  - All test-writing tasks marked [P] can run in parallel (different test files/functions)
  - CLI helper functions marked [P] can run in parallel (different concerns)
- **Phase 7 (Polish)**: T081-T087, T091 can run in parallel (different files)
- **Different user stories** can be worked on in parallel by different team members (after Foundational phase)

---

## Parallel Example: User Story 1

```bash
# Red Phase - Write all tests in parallel:
Task T013: Write Task dataclass test
Task T014: Write add_task() ID assignment test
Task T015: Write add_task() validation test
Task T016: Write get_all_tasks() empty list test
Task T017: Write get_all_tasks() sorted test
Task T018: Write integration test

# Then sequentially:
Task T019: Run pytest (verify FAIL)

# Green Phase - Implementation (some parallel):
Task T020: Implement Task dataclass
Task T021: Implement TaskManager.__init__
Task T022: Implement add_task()
Task T023: Implement get_all_tasks()
Task T024: Run pytest (verify unit tests PASS)

# CLI parallel:
Task T025: get_string_input() helper
Task T026: format_task_list() helper
Task T027: format_status_indicator() helper

# Then sequential:
Task T028: add_task_command()
Task T029: view_tasks_command()
Task T030: main() with menu
Task T031: Run pytest (verify integration PASS)

# Refactor Phase:
Task T032: Refactor validation
Task T033: PEP 8 & type hints
Task T034: Run pytest (confirm still PASS)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T009)
2. Complete Phase 2: Foundational (T010-T012, checkpoint)
3. Complete Phase 3: User Story 1 (T013-T034)
4. **STOP and VALIDATE**: Test User Story 1 independently, manually verify add/view workflow
5. Deploy/demo if ready - users can now add and view tasks

### Incremental Delivery

1. **Foundation ready** (Setup + Foundational) → T001-T012 complete
2. **MVP** (Add User Story 1) → T013-T034 → Test independently → Deploy/Demo
3. **V1.1** (Add User Story 2) → T035-T049 → Test independently → Deploy/Demo
4. **V1.2** (Add User Story 3) → T050-T065 → Test independently → Deploy/Demo
5. **V1.3** (Add User Story 4) → T066-T080 → Test independently → Deploy/Demo
6. **V2.0** (Polish) → T081-T092 → Full validation → Final release

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T012)
2. Once Foundational is done (checkpoint passed):
   - Developer A: User Story 1 (T013-T034)
   - Developer B: User Story 2 (T035-T049) - can start once T010-T012 complete
   - Developer C: User Story 3 (T050-T065) - can start once T010-T012 complete
   - Developer D: User Story 4 (T066-T080) - can start once T010-T012 complete
3. Stories complete and integrate independently
4. Team collaborates on Polish (T081-T092)

---

## TDD Checkpoints (Constitution Compliance)

**Red-Green-Refactor cycle MUST be followed** per Constitution Principle III:

### Red Phase Checkpoints
- [ ] T019: User Story 1 tests FAIL before implementation
- [ ] T040: User Story 2 tests FAIL before implementation
- [ ] T056: User Story 3 tests FAIL before implementation
- [ ] T071: User Story 4 tests FAIL before implementation

### Green Phase Checkpoints
- [ ] T024: User Story 1 unit tests PASS after service implementation
- [ ] T031: User Story 1 integration tests PASS after CLI implementation
- [ ] T043: User Story 2 unit tests PASS after service implementation
- [ ] T047: User Story 2 integration tests PASS after CLI implementation
- [ ] T060: User Story 3 unit tests PASS after service implementation
- [ ] T063: User Story 3 integration tests PASS after CLI implementation
- [ ] T074: User Story 4 unit tests PASS after service implementation
- [ ] T078: User Story 4 integration tests PASS after CLI implementation

### Refactor Phase Checkpoints
- [ ] T034: User Story 1 tests still PASS after refactoring
- [ ] T049: User Story 2 tests still PASS after refactoring
- [ ] T065: User Story 3 tests still PASS after refactoring
- [ ] T080: User Story 4 tests still PASS after refactoring

**CRITICAL**: Each checkpoint MUST be verified before proceeding. Skipping verification violates Constitution Principle III and risks broken functionality.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **Verify tests FAIL before implementing** (Red phase - critical TDD step)
- **Verify tests PASS after implementing** (Green phase)
- **Verify tests still PASS after refactoring** (Refactor phase)
- Commit after each task or logical group (Red-Green-Refactor cycle completion)
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Count Summary

- **Phase 1 (Setup)**: 9 tasks
- **Phase 2 (Foundational)**: 3 tasks
- **Phase 3 (User Story 1)**: 22 tasks (7 tests, 12 implementation, 3 refactor)
- **Phase 4 (User Story 2)**: 15 tasks (6 tests, 7 implementation, 2 refactor)
- **Phase 5 (User Story 3)**: 16 tasks (7 tests, 7 implementation, 2 refactor)
- **Phase 6 (User Story 4)**: 15 tasks (6 tests, 6 implementation, 2 refactor)
- **Phase 7 (Polish)**: 12 tasks

**Total**: 92 tasks

**Test Tasks**: 26 (28% - reflects TDD-first approach)
**Implementation Tasks**: 54 (59%)
**Refactor/Polish Tasks**: 12 (13%)

**Parallel Opportunities**: 35 tasks marked [P] (38% can run in parallel given proper team distribution)

**MVP Scope** (User Story 1 only): 34 tasks (Setup + Foundational + US1 = T001-T034)
