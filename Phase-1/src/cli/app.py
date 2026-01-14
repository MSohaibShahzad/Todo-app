"""Main application entry point for Todo console app."""

from src.services.task_manager import TaskManager
from src.cli.menu import (
    add_task_command,
    view_tasks_command,
    mark_complete_command,
    mark_incomplete_command,
    update_task_command,
    delete_task_command,
    search_tasks_command,
    filter_tasks_command,
)


def display_menu() -> None:
    """Display the main menu options."""
    print("\n=== Todo Application ===")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Mark Task Incomplete")
    print("7. Search Tasks")
    print("8. Filter Tasks")
    print("9. Exit")


def display_startup_notifications(manager: TaskManager) -> None:
    """Display startup notifications for overdue and upcoming tasks.

    Args:
        manager: TaskManager instance to check for due dates
    """
    overdue = manager.get_overdue_tasks()
    due_today = manager.get_tasks_due_today()
    upcoming = manager.get_upcoming_tasks(days=1)  # Tasks due tomorrow

    if overdue or due_today or upcoming:
        print("\n⏰ Task Reminders:")
        if overdue:
            print(f"  • {len(overdue)} task(s) OVERDUE")
        if due_today:
            print(f"  • {len(due_today)} task(s) due TODAY")
        if upcoming:
            print(f"  • {len(upcoming)} task(s) due TOMORROW")
        print()


def main() -> None:
    """Main application entry point.

    Behavior:
        - Create TaskManager instance
        - Display welcome message
        - Display startup notifications for due dates
        - Enter main menu loop
        - Handle user commands
        - Exit cleanly on option 9
    """
    manager = TaskManager()

    print("Welcome to Todo Application!")
    print("All data is stored in memory only and will be lost when you exit.")

    # Display startup notifications
    display_startup_notifications(manager)

    while True:
        display_menu()

        try:
            choice = input("\nEnter choice (1-9): ").strip()

            if choice == "1":
                add_task_command(manager)
            elif choice == "2":
                view_tasks_command(manager)
            elif choice == "3":
                update_task_command(manager)
            elif choice == "4":
                delete_task_command(manager)
            elif choice == "5":
                mark_complete_command(manager)
            elif choice == "6":
                mark_incomplete_command(manager)
            elif choice == "7":
                search_tasks_command(manager)
            elif choice == "8":
                filter_tasks_command(manager)
            elif choice == "9":
                print("\nGoodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 9.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
