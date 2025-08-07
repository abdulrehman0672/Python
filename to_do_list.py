task_list=[]


def add_task(task):
    """Add a task to the task list."""
    task_list.append(task)


def remove_task(task):
    """Remove a task from the task list."""
    if task in task_list:
        task_list.remove(task)
    else:
        print(f"Task '{task}' not found in the list.")

def view_tasks():
    """View all tasks in the task list."""
    if not task_list:
        print("No tasks in the list.")
    else:
        print("Tasks in the list:")
        for task in task_list:
            print(f"- {task}")

def main():
    print("Welcome to the To-Do List Manager!")
    while True:
        print("\nOptions:")
        print("1. Add a task")
        print("2. Remove a task")
        print("3. View tasks")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")
        if choice == '1':
            task = input("Enter the task to add: ")
            add_task(task)
        elif choice == '2':
            task = input("Enter the task to remove: ")
            remove_task(task)
        elif choice == '3':
            view_tasks()
        elif choice == '4':
            print("Exiting the To-Do List Manager. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 4.")

main()