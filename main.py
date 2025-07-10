#!/usr/bin/env python3
"""
AI Daily Planner - Main Entry Point

A productivity tool that generates an optimal daily schedule using AI.
"""
import argparse
import sys
from datetime import datetime, date
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.absolute()))

from config.config import Config
from planner.agent import PlanningAgent
from planner.preferences import PlanningPreferences, load_preferences, save_preferences
from io_modules.input_parser import get_task_input, format_tasks_for_display
from io_modules.output_writer import save_to_markdown, save_tasks_to_markdown
from memory.db import save_plan, get_plan, get_recent_plans, init_db

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='AI Daily Planner')
    parser.add_argument('--tasks', action='store_true', help='Enter tasks interactively (default)')
    parser.add_argument('--view', action='store_true', help="View today's plan")
    parser.add_argument('--recent', type=int, nargs='?', const=3, help='View recent N plans (default: 3)')
    parser.add_argument('--date', type=str, help='View plan for specific date (YYYY-MM-DD)')
    parser.add_argument('--prefs', action='store_true', help='Edit preferences')
    return parser.parse_args()

def initialize_environment():
    """Initialize the application environment."""
    # Create necessary directories
    Path("DailyPlans").mkdir(exist_ok=True)
    
    # Initialize database
    init_db()

def edit_preferences():
    """Interactively edit user preferences."""
    print("\n✏️  Edit Planning Preferences")
    print("Leave blank to keep current values.")
    
    prefs = load_preferences()
    
    print(f"\nCurrent workday: {prefs.workday_start} - {prefs.workday_end}")
    new_workday = input("Enter workday hours (e.g., 09:00-17:30): ").strip()
    if new_workday and '-' in new_workday:
        start, end = new_workday.split('-')
        prefs.workday_start = start.strip()
        prefs.workday_end = end.strip()
    
    print(f"\nCurrent max time block: {prefs.max_time_block} minutes")
    new_max_block = input("Enter max time block in minutes (default 90): ").strip()
    if new_max_block.isdigit():
        prefs.max_time_block = int(new_max_block)
    
    print(f"\nCurrent break interval: {prefs.break_interval} minutes")
    new_break = input("Enter break interval in minutes (default 15): ").strip()
    if new_break.isdigit():
        prefs.break_interval = int(new_break)
    
    print(f"\nDeep work in morning: {'Yes' if prefs.deep_work_morning else 'No'}")
    deep_work = input("Schedule deep work in morning? (y/n, default y): ").strip().lower()
    if deep_work in ['y', 'n']:
        prefs.deep_work_morning = (deep_work == 'y')
    
    save_preferences(prefs)
    print("\n✅ Preferences saved!")
    return prefs

def view_plan(plan_date: str = None):
    """View a saved plan."""
    plan = get_plan(plan_date or str(date.today()))
    if not plan:
        print(f"\n❌ No plan found for {plan_date or 'today'}")
        return False
    
    print("\n" + "="*50)
    print(f"📅 PLAN - {plan_date or 'TODAY'}")
    print("="*50)
    print(plan['schedule'])
    print("\n💡 Schedule Rationale:")
    print(plan['reasoning'])
    return True

def view_recent_plans(limit: int = 3):
    """View recent plans."""
    plans = get_recent_plans(limit)
    if not plans:
        print("\n❌ No plans found in the database.")
        return
    
    print(f"\n📅 Last {len(plans)} Plans")
    print("-" * 50)
    
    for i, plan in enumerate(plans, 1):
        print(f"{i}. {plan['date']} - {plan['schedule'][:50]}...")
    
    try:
        choice = input("\nEnter plan number to view (or press Enter to continue): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(plans):
            plan = plans[int(choice) - 1]
            print("\n" + "="*50)
            print(f"📅 Plan for {plan['date']}")
            print("="*50)
            print(plan['schedule'])
            print("\n💡 Schedule Rationale:")
            print(plan['reasoning'])
            input("\nPress Enter to continue...")
    except (ValueError, KeyboardInterrupt):
        pass

def generate_schedule(agent, preferences):
    """Generate and display a schedule."""
    try:
        # Get tasks from user
        tasks = get_task_input()
        if not tasks:
            print("\n❌ No tasks provided. Exiting...")
            return
        
        # Display tasks to be scheduled
        print("\n📋 Tasks to schedule:")
        for i, task in enumerate(tasks, 1):
            if isinstance(task, dict):
                task_str = task.get('task', 'Unnamed task')
                if 'priority' in task and task['priority']:
                    task_str += f" | Priority: {task['priority']}"
                if 'duration' in task and task['duration']:
                    duration = f"{task['duration']} min" if isinstance(task['duration'], int) else str(task['duration'])
                    task_str += f" | Duration: {duration}"
                if 'deadline' in task and task['deadline']:
                    task_str += f" | Due: {task['deadline']}"
                print(f"{i}. {task_str}")
            else:
                print(f"{i}. {task}")
        
        # Get current time
        current_time = datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
        print(f"\n⏰ Current time: {current_time}")
        print("⏳ Generating your optimal schedule...")
        
        try:
            # Generate schedule using the agent
            schedule, rationale = agent.generate_schedule(tasks, current_time, preferences)
            
            if not schedule or not isinstance(schedule, str):
                raise ValueError("Failed to generate schedule: Invalid response from the AI model")
            
            # Get today's date as string
            today = str(date.today())
            
            # Save to database
            save_plan(today, schedule, rationale)
            
            # Export to markdown - ensure we're passing the correct parameters
            output_file = save_to_markdown(
                schedule=schedule,
                reasoning=rationale,
                date=today
            )
            
            # Display the schedule
            print("\n✅ Schedule generated successfully!")
            print(f"\n📅 Schedule saved to: {output_file}")
            print("\n" + "="*50)
            print(schedule)
            print("="*50 + "\n")
            
        except Exception as e:
            error_msg = str(e)
            if "rate limit" in error_msg.lower():
                print("\n❌ Error: You've hit the rate limit for the OpenAI API.")
                print("Please wait a few minutes and try again, or check your API usage at:")
                print("https://platform.openai.com/account/usage")
            elif "authentication" in error_msg.lower() or "invalid api key" in error_msg.lower():
                print("\n❌ Error: Invalid OpenAI API key.")
                print("Please check that your OPENAI_API_KEY in the .env file is correct.")
                print("You can generate a new API key at: https://platform.openai.com/api-keys")
            else:
                print(f"\n❌ Error generating schedule: {error_msg}")
                print("\nPlease check your input and try again. If the problem persists, ")
                print("you may want to simplify your tasks or try again later.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")
        print("\nPlease try again or report this issue if it continues.")

def main():
    """Main entry point for the AI Daily Planner."""
    try:
        # Initialize environment
        initialize_environment()
        
        # Parse command line arguments
        args = parse_arguments()
        
        # Handle preference editing
        if args.prefs:
            edit_preferences()
            return
        
        # Handle viewing plans
        if args.view:
            view_plan()
            return
            
        if args.date:
            view_plan(args.date)
            return
            
        if args.recent is not None:
            view_recent_plans(args.recent)
            return
        
        # Default action: generate a new schedule
        try:
            # Load preferences
            preferences = load_preferences()
            
            # Initialize the planning agent
            agent = PlanningAgent()
            
            # Generate and display the schedule
            generate_schedule(agent, preferences)
            
        except ValueError as e:
            if "OPENAI_API_KEY" in str(e):
                print("\n❌ Error: OpenAI API key not found.")
                print("Please ensure you have set up your OPENAI_API_KEY in the .env file.")
                print("The .env file should be in the project root and contain:")
                print("OPENAI_API_KEY=your_api_key_here\n")
            else:
                print(f"\n❌ Error: {str(e)}")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {str(e)}")
            print("\nPlease check your internet connection and try again.")
            print("If the problem persists, please report this issue.")
            
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")

if __name__ == "__main__":
    main()
