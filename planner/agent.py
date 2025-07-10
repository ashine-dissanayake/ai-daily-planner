"""Agent implementation for the AI Daily Planner."""
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from config.config import Config
from planner.prompt import get_schedule_prompt
from planner.preferences import PlanningPreferences

class PlanningAgent:
    """Agent responsible for generating and managing daily schedules using LLMs."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the planning agent with configuration.
        
        Args:
            config: Optional Config object with API settings
        """
        self.config = config or Config()
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize the language model with configuration."""
        return ChatOpenAI(
            model_name=self.config.MODEL_NAME,
            temperature=self.config.TEMPERATURE,
            max_tokens=self.config.MAX_TOKENS,
            openai_api_key=self.config.OPENAI_API_KEY
        )
    
    def generate_schedule(
        self, 
        tasks: List[Dict[str, Any]], 
        current_time: Optional[str] = None,
        preferences: Optional[PlanningPreferences] = None
    ) -> Tuple[str, str]:
        """
        Generate a time-blocked schedule from a list of tasks.
        
        Args:
            tasks: List of task dictionaries to schedule
            current_time: Optional current time string (defaults to now)
            preferences: Optional PlanningPreferences object
            
        Returns:
            A tuple of (schedule, rationale) where:
            - schedule: The formatted time-blocked schedule
            - rationale: The AI's reasoning for the schedule
            
        Raises:
            ValueError: If the LLM response is invalid or empty
            Exception: For other errors during schedule generation
        """
        if not tasks:
            raise ValueError("No tasks provided for scheduling")
            
        if current_time is None:
            current_time = datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
        
        try:
            # Format tasks for the prompt
            tasks_str = self.format_tasks(tasks)
            
            # Get preferences as dict if provided
            prefs_dict = preferences.to_dict() if preferences else {}
            
            # Create the chain with the prompt
            prompt = get_schedule_prompt(prefs_dict)
            chain = LLMChain(
                llm=self.llm,
                prompt=prompt,
                verbose=True
            )
            
            # Generate the schedule using the LLM chain
            print("\n🤖 Generating schedule with AI...")  # User feedback
            result = chain.run({
                "tasks": tasks_str,
                "current_time": current_time,
                "preferences": str(prefs_dict) if prefs_dict else "None"
            })
            
            if not result or not isinstance(result, str):
                raise ValueError("Received empty or invalid response from the AI model")
                
            # Clean up the response
            result = result.strip()
            
            # Split the result into schedule and rationale sections
            if "## Schedule Rationale" in result:
                schedule, rationale = result.split("## Schedule Rationale", 1)
                schedule = schedule.strip()
                rationale = rationale.strip()
                
                # Validate the schedule format
                if not schedule or len(schedule) < 10:  # Basic validation
                    raise ValueError("Generated schedule is too short or invalid")
                    
                return schedule, rationale
                
            # If no explicit rationale section, use the whole response as schedule
            if len(result) > 50:  # Basic validation
                return result, "No detailed rationale provided."
                
            raise ValueError("Generated schedule is too short or invalid")
            
        except Exception as e:
            error_msg = str(e)
            print(f"\n⚠️ Error during schedule generation: {error_msg}")
            raise  # Re-raise to be handled by the caller
    
    @staticmethod
    def format_tasks(task_list: List[Dict[str, Any]]) -> str:
        """
        Format a list of task dictionaries into a string for the LLM.
        
        Args:
            task_list: List of task dictionaries with keys:
                      - task: str (required)
                      - priority: str (optional)
                      - duration: str/int (optional)
                      - deadline: str (optional)
                      - notes: str (optional)
            
        Returns:
            Formatted string of tasks
        """
        formatted = []
        for i, task in enumerate(task_list, 1):
            task_info = [f"{i}. {task.get('task', 'Unnamed task')}"]
            
            # Add priority if available
            if 'priority' in task and task['priority']:
                priority = task['priority']
                if priority.lower() in ['high', 'medium', 'low']:
                    priority = priority.capitalize()
                task_info.append(f"Priority: {priority}")
            
            # Add duration if available
            if 'duration' in task and task['duration']:
                duration = task['duration']
                if isinstance(duration, int):
                    duration = f"{duration} min"
                task_info.append(f"Duration: {duration}")
            
            # Add deadline if available
            if 'deadline' in task and task['deadline']:
                task_info.append(f"Due: {task['deadline']}")
            
            # Add any additional notes
            if 'notes' in task and task['notes']:
                task_info.append(f"Notes: {task['notes']}")
            
            formatted.append(" | ".join(task_info))
        
        return "\n".join(formatted) if formatted else "No tasks provided."
