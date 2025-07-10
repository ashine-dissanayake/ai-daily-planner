"""Module for writing schedule output to markdown files."""
from pathlib import Path
from datetime import datetime
import os
from typing import Optional

def ensure_directory(path: str) -> Path:
    """Ensure the directory exists, create if it doesn't."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def save_to_markdown(
    schedule: str, 
    reasoning: str, 
    output_dir: str = "DailyPlans",
    date: Optional[str] = None
) -> str:
    """
    Save schedule and reasoning to a markdown file.
    
    Args:
        schedule: The formatted schedule
        reasoning: The reasoning behind the schedule
        output_dir: Directory to save the markdown file
        date: Optional date string (YYYY-MM-DD). Uses today if None.
        
    Returns:
        Path to the saved markdown file
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Ensure output directory exists
    output_path = ensure_directory(output_dir)
    
    # Create filename
    filename = f"{date}.md"
    filepath = output_path / filename
    
    # Format markdown content
    content = f"# 📅 Daily Plan - {date}\n\n"
    content += "## 🗓 Schedule\n\n"
    content += f"{schedule}\n\n"
    content += "## 💭 Reasoning\n\n"
    content += f"{reasoning}\n"
    
    # Write to file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(filepath.absolute())
    except IOError as e:
        print(f"Error writing to file {filepath}: {e}")
        return ""

def save_tasks_to_markdown(
    tasks: list, 
    output_dir: str = "DailyPlans",
    filename: str = "tasks.md"
) -> str:
    """
    Save a list of tasks to a markdown file.
    
    Args:
        tasks: List of task dictionaries
        output_dir: Directory to save the markdown file
        filename: Name of the output file
        
    Returns:
        Path to the saved markdown file
    """
    # Ensure output directory exists
    output_path = ensure_directory(output_dir)
    filepath = output_path / filename
    
    # Format markdown content
    content = "# 📋 Tasks\n\n"
    
    for i, task in enumerate(tasks, 1):
        task_line = f"- [ ] {task.get('task', 'Unnamed task')}"
        if 'priority' in task:
            task_line += f" *(Priority: {task['priority']})*"
        if 'duration' in task:
            task_line += f" ⏱ {task['duration']}"
        if 'deadline' in task:
            task_line += f" ⏰ {task['deadline']}"
        content += task_line + "\n"
    
    # Write to file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(filepath.absolute())
    except IOError as e:
        print(f"Error writing to file {filepath}: {e}")
        return ""
