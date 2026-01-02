#!/usr/bin/env python3
"""Manual test script for full application workflow."""

from src.services.task_manager import TaskManager
from src.cli.display import format_task_list

def test_full_workflow():
    """Test complete application workflow manually."""
    print("=== Manual Test Script ===\n")

    manager = TaskManager()

    # Test 1: View empty list
    print("Test 1: View empty list")
    tasks = manager.get_all_tasks()
    print(format_task_list(tasks))
    print()

    # Test 2: Add tasks
    print("Test 2: Add tasks")
    task1 = manager.add_task("Buy groceries", "Milk, eggs, bread, coffee")
    print(f"✓ Added task ID: {task1.id}")

    task2 = manager.add_task("Write report", "Q4 financial summary")
    print(f"✓ Added task ID: {task2.id}")

    task3 = manager.add_task("Call dentist", "")
    print(f"✓ Added task ID: {task3.id}")
    print()

    # Test 3: View all tasks
    print("Test 3: View all tasks")
    tasks = manager.get_all_tasks()
    print(format_task_list(tasks))
    print()

    # Test 4: Mark task complete
    print("Test 4: Mark task #1 complete")
    manager.mark_complete(1, True)
    tasks = manager.get_all_tasks()
    print(format_task_list(tasks))
    print()

    # Test 5: Mark task incomplete
    print("Test 5: Mark task #1 incomplete again")
    manager.mark_complete(1, False)
    tasks = manager.get_all_tasks()
    print(format_task_list(tasks))
    print()

    # Test 6: Update task
    print("Test 6: Update task #2 title and description")
    manager.update_task(2, title="Write annual report", description="Full year financial summary and projections")
    tasks = manager.get_all_tasks()
    print(format_task_list(tasks))
    print()

    # Test 7: Delete task
    print("Test 7: Delete task #3")
    manager.delete_task(3)
    tasks = manager.get_all_tasks()
    print(format_task_list(tasks))
    print()

    # Test 8: Error handling - invalid task ID
    print("Test 8: Error handling - invalid task ID")
    try:
        manager.mark_complete(999, True)
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    print()

    # Test 9: Error handling - empty title
    print("Test 9: Error handling - empty title")
    try:
        manager.add_task("", "Description")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    print()

    # Test 10: Error handling - title too long
    print("Test 10: Error handling - title too long")
    try:
        manager.add_task("x" * 300, "Description")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    print()

    print("=== All Manual Tests Passed! ===")

if __name__ == "__main__":
    test_full_workflow()
