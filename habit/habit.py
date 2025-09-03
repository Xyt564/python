import os
from datetime import date
import json

# Get folder of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "habits.json")

# Load or create habits file
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        habits = json.load(f)
else:
    habits = {}

# rest of your code stays the same...



def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(habits, f, indent=4)


def add_habit():
    name = input("Enter habit name: ").strip()
    if name in habits:
        print("Habit alrady exsits!")
        return
    habits[name] = {}
    save_data()
    print(f"Habit '{name}' added!")


def mark_done():
    name = input("Enter habit to be marked done: ").strip()
    if name not in habits:
        print("Habit not found")
        return
    today = str(date.today())
    if today not in habits[name]:
        habits[name].append(today)
        save_data()
        print(f"Marked '{name}' as done for today")
    else:
        print("Already marked done today")


def view_progress():
    for habit, days in habits.items():
        print(f"\n{habit}:")
        print(f" Days completed: {len(days)}")
        chart = "█" * len(days) + "░" * (10 - len(days))
        print(f"  Progress: {chart}")

def main():
    while True:
        print("\n ---Habit Tracker---")
        print("1. Add Habit")
        print("2. Mark Habit Done")
        print("3. View Progress")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_habit()
        elif choice == "2":
            mark_done()
        elif choice == "3":
            view_progress()
        elif choice == "4":
            break
        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    main()