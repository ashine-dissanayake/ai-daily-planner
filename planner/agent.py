"""Agent implementation for the AI Daily Planner."""
from typing import Dict, Tuple
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from config.config import Config
from planner.prompt import get_schedule_prompt

class PlanningAgent:
    """Agent responsible for generating and managing daily schedules using LLMs."""
    
    def __init__(self, config: Config = None):
        """Initialize the planning agent with configuration."""
        self.config = config or Config()
        self.llm = ChatOpenAI(
            model_name=self.config.MODEL_NAME,
            temperature=self.config.TEMPERATURE,
            max_tokens=self.config.MAX_TOKENS,
            openai_api_key=self.config.OPENAI_API_KEY
        )
        self.chain = self._create_chain()
    
    def _create_chain(self) -> LLMChain:
        """Create and configure the LLM chain for schedule generation."""
        prompt = get_schedule_prompt()
        return LLMChain(
            llm=self.llm,
            prompt=prompt,
            verbose=True
        )
    
    def generate_schedule(self, tasks: str, current_time: str) -> Tuple[str, str]:
        """
        Generate a time-blocked schedule from a list of tasks.
        
        Args:
            tasks: A string containing the list of tasks to schedule
            current_time: Current date and time as a string
            
        Returns:
            A tuple of (schedule, rationale) where:
            - schedule: The formatted time-blocked schedule
            - rationale: The AI's reasoning for the schedule
        """
        try:
            # Generate the schedule using the LLM chain
            result = self.chain.run({
                "tasks": tasks,
                "current_time": current_time
            })
            
            # Split the result into schedule and rationale sections
            if "## Schedule Rationale" in result:
                schedule, rationale = result.split("## Schedule Rationale", 1)
                return schedule.strip(), rationale.strip()
            return result.strip(), "No rationale provided."
            
        except Exception as e:
            error_msg = f"Error generating schedule: {str(e)}"
            return "", error_msg
    
    @staticmethod
    def format_tasks(task_list: list[Dict[str, str]]) -> str:
        """
        Format a list of task dictionaries into a string for the LLM.
        
        Args:
            task_list: List of dicts with 'task', 'priority', 'duration', 'deadline'
            
        Returns:
            Formatted string of tasks
        """
        formatted = []
        for i, task in enumerate(task_list, 1):
            task_str = f"{i}. {task['task']}"
            if 'priority' in task:
                task_str += f" (Priority: {task['priority']})"
            if 'duration' in task:
                task_str += f" - {task['duration']} min"
            if 'deadline' in task:
                task_str += f" - Due: {task['deadline']}"
            formatted.append(task_str)
        return "\n".join(formatted)
