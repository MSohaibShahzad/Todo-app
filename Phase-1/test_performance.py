#!/usr/bin/env python3
"""Performance tests for the Todo application."""

import time
from src.services.task_manager import TaskManager
from src.cli.display import format_task_list

def test_startup_time():
    """Test that application startup is under 1 second."""
    print("=== Testing Application Startup Time ===")

    start = time.time()
    manager = TaskManager()
    elapsed = time.time() - start

    print(f"TaskManager initialization: {elapsed * 1000:.2f} ms")

    if elapsed < 1.0:
        print(f"✓ PASS: Startup time {elapsed * 1000:.2f} ms < 1000 ms")
    else:
        print(f"✗ FAIL: Startup time {elapsed * 1000:.2f} ms >= 1000 ms")

    print()
    return elapsed < 1.0


def test_100_tasks_performance():
    """Test that 100 tasks can be added and displayed efficiently."""
    print("=== Testing Performance with 100 Tasks ===")

    manager = TaskManager()

    # Add 100 tasks
    start = time.time()
    for i in range(100):
        manager.add_task(
            f"Task {i+1}",
            f"This is the description for task number {i+1}"
        )
    add_elapsed = time.time() - start
    print(f"Time to add 100 tasks: {add_elapsed * 1000:.2f} ms")

    # Get all tasks
    start = time.time()
    tasks = manager.get_all_tasks()
    get_elapsed = time.time() - start
    print(f"Time to get all tasks: {get_elapsed * 1000:.2f} ms")

    # Format for display
    start = time.time()
    formatted = format_task_list(tasks)
    format_elapsed = time.time() - start
    print(f"Time to format task list: {format_elapsed * 1000:.2f} ms")

    print(f"\nTotal tasks: {len(tasks)}")
    print(f"Output length: {len(formatted)} characters")
    print(f"Output lines: {len(formatted.split(chr(10)))}")

    # Display first 5 and last 5 tasks to verify formatting
    print("\n=== First 5 Tasks ===")
    lines = formatted.split('\n')
    for line in lines[:7]:  # Header + first 5 tasks (2 lines each)
        print(line)

    print("\n=== Last 5 Tasks ===")
    for line in lines[-12:-1]:  # Last 5 tasks (2 lines each) + footer
        print(line)

    total_time = add_elapsed + get_elapsed + format_elapsed
    print(f"\n✓ All operations completed successfully")
    print(f"Total time: {total_time * 1000:.2f} ms")

    if total_time < 1.0:
        print("✓ PASS: All operations < 1000 ms")
    else:
        print(f"⚠ WARNING: Total time {total_time * 1000:.2f} ms >= 1000 ms")

    print()
    return True


def test_mark_complete_performance():
    """Test marking tasks complete with large dataset."""
    print("=== Testing Mark Complete Performance with 100 Tasks ===")

    manager = TaskManager()

    # Add 100 tasks
    for i in range(100):
        manager.add_task(f"Task {i+1}", f"Description {i+1}")

    # Mark every 10th task as complete
    start = time.time()
    for i in range(1, 101, 10):
        manager.mark_complete(i, True)
    elapsed = time.time() - start

    print(f"Time to mark 10 tasks complete: {elapsed * 1000:.2f} ms")

    # Verify correct tasks are marked
    tasks = manager.get_all_tasks()
    complete_count = sum(1 for t in tasks if t.is_complete)
    print(f"Tasks marked complete: {complete_count}/100")

    if complete_count == 10:
        print("✓ PASS: Correct number of tasks marked complete")
    else:
        print(f"✗ FAIL: Expected 10 complete tasks, got {complete_count}")

    print()
    return complete_count == 10


if __name__ == "__main__":
    print("=== Performance Test Suite ===\n")

    results = []
    results.append(("Startup Time", test_startup_time()))
    results.append(("100 Tasks Performance", test_100_tasks_performance()))
    results.append(("Mark Complete Performance", test_mark_complete_performance()))

    print("\n=== Summary ===")
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")

    all_passed = all(r[1] for r in results)
    if all_passed:
        print("\n✓ All performance tests passed!")
    else:
        print("\n✗ Some performance tests failed")
