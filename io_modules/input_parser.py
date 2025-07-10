"""Module for parsing task input from the command line."""
from typing import List, Dict, Optional

def get_task_input() -> List[Dict[str, str]]:
    """
    Prompt user to input tasks one by line until an empty line is entered.
    
    Returns:
        List of task dictionaries with 'task' key and optional metadata.
    """
    print("\n📝 Enter your tasks (press Enter twice when done):")
    print("Format: Task name [priority=High|Medium|Low] [duration=Xmin] [due=HH:MM]")
    print("Example: Write project report priority=High duration=120 due=18:00\n")
    
    tasks = []
    while True:
        try:
            line = input("• ").strip()
            if not line and tasks:  # Empty line ends input if at least one task exists
                break
            if not line:  # Skip empty lines at start
                continue
                
            task = {"task": line}
            
            # Parse optional parameters
            parts = line.split()
            task_text = []
            
            for part in parts[1:]:  # Skip the first word (task name)
                if '=' in part:
                    key, value = part.split('=', 1)
                    if key == 'priority' and value.lower() in ['high', 'medium', 'low']:
                        task['priority'] = value.capitalize()
                    elif key == 'duration' and value.lower().endswith('min'):
                        task['duration'] = value
                    elif key == 'due':
                        task['deadline'] = value
                    continue
                task_text.append(part)
            
            # Rebuild the task text without the parsed parameters
            task['task'] = f"{parts[0]} {' '.join(task_text)}".strip()
            tasks.append(task)
            
        except KeyboardInterrupt:
            print("\nInput cancelled.")
            return []
        except Exception as e:
            print(f"Error parsing input: {e}")
            continue
            
    return tasks

def format_tasks_for_display(tasks: List[Dict[str, str]]) -> str:
    """Format tasks for display in the terminal."""
    if not tasks:
        return "No tasks provided."
        
    formatted = []
    for i, task in enumerate(tasks, 1):
        task_str = f"{i}. {task['task']}"
        if 'priority' in task:
            task_str += f" (Priority: {task['priority']})"
        if 'duration' in task:
            task_str += f" - {task['duration']}"
        if 'deadline' in task:
            task_str += f" - Due: {task['deadline']}"
        formatted.append(task_str)
    
    return "\n".join(formatted)
