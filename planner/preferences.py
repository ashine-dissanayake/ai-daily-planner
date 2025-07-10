"""Module for managing planning preferences and configurations."""
from dataclasses import dataclass
from typing import Optional
from datetime import time
import json
import os

@dataclass
class PlanningPreferences:
    """Stores user preferences for scheduling."""
    workday_start: str = "09:00"
    workday_end: str = "18:00"
    max_time_block: int = 90  # minutes
    break_interval: int = 15  # minutes
    deep_work_morning: bool = True
    
    def to_dict(self) -> dict:
        """Convert preferences to a dictionary."""
        return {
            "workday_start": self.workday_start,
            "workday_end": self.workday_end,
            "max_time_block": self.max_time_block,
            "break_interval": self.break_interval,
            "deep_work_morning": self.deep_work_morning
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PlanningPreferences':
        """Create preferences from a dictionary."""
        return cls(**data)
    
    def to_prompt_context(self) -> str:
        """Format preferences for the LLM prompt."""
        return (
            f"Workday: {self.workday_start} - {self.workday_end}\n"
            f"Maximum time block: {self.max_time_block} minutes\n"
            f"Break interval: {self.break_interval} minutes\n"
            f"Deep work preference: {'Morning' if self.deep_work_morning else 'Afternoon'}"
        )

def load_preferences(config_path: str = "preferences.json") -> PlanningPreferences:
    """Load preferences from a JSON file or return defaults."""
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return PlanningPreferences.from_dict(json.load(f))
        except Exception as e:
            print(f"Warning: Could not load preferences: {e}")
    return PlanningPreferences()

def save_preferences(prefs: PlanningPreferences, config_path: str = "preferences.json") -> None:
    """Save preferences to a JSON file."""
    try:
        with open(config_path, 'w') as f:
            json.dump(prefs.to_dict(), f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save preferences: {e}")

# Default preferences
DEFAULT_PREFERENCES = PlanningPreferences()
