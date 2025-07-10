"""Prompt templates for the AI Daily Planner."""
from langchain_core.prompts import PromptTemplate
from typing import Optional

def get_system_message(preferences: Optional[dict] = None) -> str:
    """Generate the system message with optional preferences."""
    base_message = """You are an expert productivity assistant that creates optimal daily schedules. 
Given a list of tasks, your job is to create a time-blocked schedule that maximizes productivity 
while considering task priorities, estimated durations, and energy levels throughout the day.

Guidelines:
1. Allocate focused time blocks (30-90 minutes) with short breaks between
2. Schedule high-priority tasks during peak energy hours
3. Group similar tasks together
4. Include buffer time between tasks
5. Be realistic about what can be accomplished in a day
6. Consider any provided preferences for work hours and scheduling constraints

Return the schedule in the specified format below."""

    if preferences:
        base_message += "\n\nUser Preferences:\n"
        for key, value in preferences.items():
            base_message += f"- {key}: {value}\n"
    
    return base_message

def get_schedule_prompt(preferences: Optional[dict] = None) -> PromptTemplate:
    """Get the schedule generation prompt with system message included.
    
    Args:
        preferences: Optional dictionary of user preferences
    """
    system_message = get_system_message(preferences)
    
    return PromptTemplate(
        input_variables=["tasks", "current_time"],
        template="""{system_message}

Current time: {current_time}

Tasks to schedule:
{tasks}

Please create a time-blocked schedule for today. For each time block, include:
- Start and end time (in 24-hour format)
- Task name and brief description
- Priority level (High/Medium/Low)
- Estimated duration
- Any relevant notes or dependencies

Also provide a detailed rationale explaining your scheduling decisions, including:
- Why tasks were scheduled at specific times
- How you prioritized between competing tasks
- Any assumptions made about task durations or dependencies
- How you've optimized for productivity and focus

Format your response as follows:

## Today's Schedule

[Start Time] - [End Time]  [Task Name] (Priority: [H/M/L], Duration: [X] min)
  • Description: [Brief description of the task]
  • Notes: [Any additional context or dependencies]
  • Rationale: [Why this time slot was chosen]

## Schedule Rationale
[Your detailed reasoning for the schedule, including:
 - Overall strategy for the day
 - How you handled priorities and dependencies
 - Any trade-offs made
 - Suggestions for optimizing the schedule]

Let's begin:
## Today's Schedule"""
    ).partial(system_message=system_message)
