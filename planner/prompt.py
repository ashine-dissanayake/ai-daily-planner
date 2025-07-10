"""Prompt templates for the AI Daily Planner."""
from langchain_core.prompts import PromptTemplate

# System message that sets the behavior of the AI
SYSTEM_MESSAGE = """You are an expert productivity assistant that creates optimal daily schedules. 
Given a list of tasks, your job is to create a time-blocked schedule that maximizes productivity 
while considering task priorities, estimated durations, and energy levels throughout the day.

Guidelines:
1. Allocate focused time blocks (30-90 minutes) with short breaks between
2. Schedule high-priority tasks during peak energy hours (typically morning)
3. Group similar tasks together
4. Include buffer time between tasks
5. Ensure all tasks fit within working hours (9 AM - 6 PM by default)
6. Be realistic about what can be accomplished in a day

Return the schedule in the specified format."""

# Main prompt template for schedule generation
SCHEDULE_PROMPT = PromptTemplate(
    input_variables=["tasks", "current_time"],
    template="""{system_message}

Current time: {current_time}

Tasks to schedule:
{tasks}

Please create a time-blocked schedule for today. For each time block, include:
- Start and end time
- Task name and description
- Priority level (High/Medium/Low)
- Estimated duration

Also provide a brief rationale explaining your scheduling decisions.

Format your response as follows:

## Today's Schedule

[Time] - [Task Name] (Priority: [H/M/L], Duration: [X] min)
  • Description: [Brief description]
  • Rationale: [Why this time slot was chosen]

## Schedule Rationale
[Your detailed reasoning for the schedule]

Let's begin:
## Today's Schedule"""
)

def get_schedule_prompt() -> PromptTemplate:
    """Get the schedule generation prompt with system message included."""
    return SCHEDULE_PROMPT.partial(system_message=SYSTEM_MESSAGE)
