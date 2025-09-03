import json
import os
import platform

FILE_NAME = "tasks.json"

def clear_screen():
    if platform.system() == "windows":
        os.system("cls")
    else:
        os.system("clear")

def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, 'r') as f:
                content = f.read().strip()
                if not content:
                    return []  # Empty file, return empty list
                return json.loads(content)
        except (json.JSONDecodeError, ValueError):
            print("Warning: Could not read tasks.json, resetting it.")
            return []
    return []

def save_tasks(tasks):
    with open(FILE_NAME, 'w') as f:
        json.dump(tasks, f, indent=2)

def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks yet.")
    else:
        print("\nYour Tasks:")
        for i, task in enumerate(tasks, start=1):
            status = "✅" if task['completed'] else "❌"
            print(f"{i}. [{status}] {task['title']}")


def add_task(tasks):
    title = input("enter task title: ").strip()
    if title:
        tasks.append({'title': title, 'completed': False})
        save_tasks(tasks)
        print("Task added")
    else:
        print("Task title cannot be empty")


def delete_task(tasks):
    show_tasks(tasks)
    try:
        index = int(input("Enter task number to delete: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks(tasks)
            print (f"Deleted task: {removed['title']}")
        else:
            print("Invalid task number")
    except ValueError:
        print("Please enter a valid number.")

def mark_complete(tasks):
    show_tasks(tasks)
    try:
        index = int(input("Enter task number to mark complete: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]['completed'] = True
            save_tasks(tasks)
            print(f"Marked task '{tasks[index]['title']}' as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def main():
    tasks = load_tasks()
    while True:
        clear_screen()  # Clear screen before showing the menu

        print("==== To-Do List Menu ====")
        print("1) Add Task")
        print("2) Delete Task")
        print("3) Mark Task as Complete")
        print("4) Show Tasks")
        print("5) Quit")
        choice = input("Choose an option (1-5): ").strip()

        # Only clear screen before doing an action — NOT immediately
        if choice == '1':
            clear_screen()
            add_task(tasks)
        elif choice == '2':
            clear_screen()
            delete_task(tasks)
        elif choice == '3':
            clear_screen()
            mark_complete(tasks)
        elif choice == '4':
            clear_screen()
            show_tasks(tasks)
            input("\nPress Enter to return to menu...")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select from 1 to 5.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

