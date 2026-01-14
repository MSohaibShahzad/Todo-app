---
id: 003
title: Phase-2 Task Generation
stage: tasks
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-intermediate-advanced-features
branch: 002-intermediate-advanced-features
user: sohaib
command: /sp.tasks
labels: ["tasks", "implementation", "tdd", "user-stories", "phase-2"]
links:
  spec: specs/002-intermediate-advanced-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-intermediate-advanced-features/tasks.md
tests:
  - Task format validation (all 106 tasks follow checklist format)
  - User story mapping (6 stories, P1-P6)
  - Dependency analysis (3 independent stories identified)
  - Parallel execution opportunities (marked with [P])
---

## Prompt

$ARGUMENTS

(No additional arguments provided - default task generation from design documents)

## Response snapshot

Generated comprehensive implementation tasks for Phase-2 intermediate and advanced features.

**Task Generation Process**:

1. **Loaded Design Documents**:
   - spec.md: 6 user stories with priorities (P1-P6) and acceptance criteria
   - data-model.md: Extended Task entity with 4 new optional fields
   - research.md: Architectural decisions (date handling, recurrence, filtering)
   - quickstart.md: TDD implementation phases
   - contracts/: Service and CLI interface contracts
   - constitution.md: Verified TDD mandate (Red-Green-Refactor required)

2. **Extracted User Stories** (priority order):
   - **US1 (P1)**: Task Prioritization - assign High/Medium/Low priorities
   - **US2 (P2)**: Task Categorization - organize into categories
   - **US3 (P3)**: Search and Filter - keyword search + multi-criteria filtering
   - **US4 (P4)**: Sort Tasks - by priority/title/due date
   - **US5 (P5)**: Due Dates & Reminders - assign due dates, console notifications
   - **US6 (P6)**: Recurring Tasks - daily/weekly/monthly auto-regeneration

3. **Mapped Entities to Stories**:
   - Task.priority → US1
   - Task.category → US2
   - search_tasks, filter_tasks → US3
   - sort_tasks → US4
   - Task.due_date, get_overdue_tasks → US5
   - Task.recurrence_rule, mark_complete (regeneration) → US6

4. **Generated Task Breakdown** (106 total tasks):
   - **Phase 1: Setup** (T001-T008) - 8 tasks
     - Install dependencies (colorama, python-dateutil)
     - Verify Phase-1 baseline
     - Create test file structure

   - **Phase 2: Foundational** (T009-T017) - 9 tasks
     - Extend Task dataclass with Phase-2 fields (TDD)
     - Verify backward compatibility

   - **Phase 3: US1 Priority** (T018-T030) - 13 tasks
     - Tests: priority validation, add/update with priority
     - Implementation: validate_priority, extend add_task/update_task
     - CLI: priority prompts, color-coded display

   - **Phase 4: US2 Category** (T031-T043) - 13 tasks
     - Tests: category validation, default "General"
     - Implementation: validate_category, extend add_task/update_task
     - CLI: category prompts, display

   - **Phase 5: US3 Search/Filter** (T044-T059) - 16 tasks
     - Tests: search (title/description), filter (status/priority/category), multi-criteria
     - Implementation: search_tasks, filter_tasks
     - CLI: Search & Filter submenu

   - **Phase 6: US4 Sort** (T060-T069) - 10 tasks
     - Tests: sort by priority/title/due_date, handle None values, ties
     - Implementation: sort_tasks with multiple keys
     - CLI: sort option in submenu

   - **Phase 7: US5 Due Dates** (T070-T087) - 18 tasks
     - Tests: due_date validation, get_overdue/due_today/upcoming
     - Implementation: validate_due_date, helper methods
     - CLI: due date prompts, startup notifications, indicators

   - **Phase 8: US6 Recurring** (T088-T103) - 16 tasks
     - Tests: recurrence validation, regeneration (daily/weekly/monthly), edge cases
     - Implementation: _calculate_next_due_date, extend mark_complete
     - CLI: recurrence prompts, recurring indicator, delete modes

   - **Phase 9: Polish** (T104-T106) - 3 tasks
     - Full test suite (≥80% coverage)
     - Integration tests
     - README update

5. **Dependency Analysis**:
   - **Independent** (can start immediately): US1, US2, US5
   - **Dependent on US1+US2**: US3 (Search/Filter needs priority and category)
   - **Dependent on US1+US5**: US4 (Sort needs priority and due_date)
   - **Dependent on US5**: US6 (Recurring needs due_date)

6. **Parallel Execution Opportunities**:
   - Marked 42 tasks with [P] for parallelizable
   - 3 independent user stories (US1, US2, US5) can be developed concurrently
   - Within each story: test writing tasks parallelizable

7. **TDD Workflow** (per user story):
   - RED phase: Write tests, verify fail
   - GREEN phase: Implement to pass tests
   - REFACTOR phase: Clean up while keeping green
   - CLI integration: Manual testing

**Task Format Validation**:
- ✅ All 106 tasks follow checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- ✅ Task IDs sequential (T001-T106)
- ✅ [P] marker on 42 parallelizable tasks
- ✅ [US1]-[US6] labels on story-specific tasks
- ✅ File paths specified for all implementation tasks
- ✅ Clear acceptance criteria per phase

**Independent Test Criteria** (per user story):
- US1: Create/update priority, view sorted, verify Medium default
- US2: Create/update category, filter by category, list categories
- US3: Search keyword, filter by status/priority/category, combine filters
- US4: Sort by priority/title/due_date, verify None handling
- US5: Assign/update due dates, view startup reminders, see indicators
- US6: Create recurring, mark complete (verify regeneration), test deletion modes

**MVP Scope**:
- Setup + Foundational + US1 (Priority) = 30 tasks
- Estimated effort: ~1.5 days
- Delivers immediate organizational value

## Outcome

- ✅ Impact: Complete task breakdown with 106 implementation tasks organized by 6 user stories. All tasks independently testable with clear acceptance criteria. TDD workflow enforced (Red-Green-Refactor).
- 🧪 Tests: 106 tasks generated, 45 are test tasks (TDD Red phase). Test coverage target ≥80% specified. Integration tests included in Polish phase.
- 📁 Files: Created tasks.md in specs/002-intermediate-advanced-features/. All tasks include specific file paths for implementation.
- 🔁 Next prompts: Begin implementation with MVP scope (T001-T030), then expand to US2/US5 in parallel, finally US3/US4/US6 and Polish.
- 🧠 Reflection: Task generation successfully organized by user story (not by technical layer). Dependencies clearly identified (US3 depends on US1+US2, US4 on US1+US5, US6 on US5). Parallel execution opportunities marked (42 tasks with [P]). Constitution TDD mandate enforced throughout. All tasks follow strict checklist format for LLM execution.

## Evaluation notes (flywheel)

- Failure modes observed: None. Initial plan.md was overwritten by template, but research.md and quickstart.md contained sufficient implementation guidance.
- Graders run and results (PASS/FAIL): Task format validation: PASS (106/106 tasks follow checklist format). User story mapping: PASS (all 6 stories mapped with priorities). Dependency analysis: PASS (3 independent stories identified). TDD compliance: PASS (constitution mandate enforced).
- Prompt variant (if applicable): Standard /sp.tasks workflow with TDD emphasis from constitution
- Next experiment (smallest change to try): Consider adding "complexity weight" to tasks for more accurate effort estimation (e.g., T097 recurrence calculation is higher complexity than T001 install dependency)
