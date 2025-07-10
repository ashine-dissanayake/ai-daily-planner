#!/usr/bin/env python3
"""
AI Daily Planner - Main Entry Point

A productivity tool that generates an optimal daily schedule using AI.
"""
import argparse
from datetime import datetime

from config.config import Config
from planner.agent import PlanningAgent

def main():
    """Main entry point for the AI Daily Planner."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AI Daily Planner')
    parser.add_argument('--tasks', type=str, help='Comma-separated list of tasks')
    args = parser.parse_args()
    
    # Example tasks (can be overridden by command line)
    example_tasks = [
        {"task": "Prepare presentation for team meeting", "priority": "High", "duration": 60},
        {"task": "Review project proposal", "priority": "Medium", "duration": 45},
        {"task": "Team standup meeting", "priority": "High", "duration": 30},
        {"task": "Code review for PR #42", "priority": "Medium", "duration": 45},
        {"task": "Lunch break", "priority": "Low", "duration": 60},
        {"task": "Work on feature X implementation", "priority": "High", "duration": 90},
        {"task": "Respond to emails", "priority": "Low", "duration": 30},
    ]
    
    # Initialize the planning agent
    try:
        agent = PlanningAgent()
        
        # Get current time in a readable format
        current_time = datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
        
        # Format tasks for the LLM
        if args.tasks:
            # Simple parsing of command line tasks
            tasks = [{"task": task.strip()} for task in args.tasks.split(",")]
        else:
            tasks = example_tasks
            
        tasks_str = agent.format_tasks(tasks)
        
        print("\n🤖 Welcome to AI Daily Planner!")
        print("📅 Current time:", current_time)
        print("\n📋 Tasks to schedule:")
        print(tasks_str)
        
        print("\n⏳ Generating your optimal schedule...")
        
        # Generate the schedule
        schedule, rationale = agent.generate_schedule(tasks_str, current_time)
        
        # Print the results
        print("\n" + "="*50)
        print("📅 YOUR OPTIMAL SCHEDULE")
        print("="*50)
        print(schedule)
        print("\n💡 Schedule Rationale:")
        print(rationale)
        print("\n✨ Have a productive day!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please ensure you have set up your OPENAI_API_KEY in the .env file.")
        print("You can get an API key from https://platform.openai.com/api-keys")

if __name__ == "__main__":
    main()
