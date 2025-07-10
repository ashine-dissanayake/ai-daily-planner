"""Configuration settings for the AI Daily Planner."""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

class Config:
    """Application configuration class."""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Model configuration
    MODEL_NAME = "gpt-4o"
    TEMPERATURE = 0.7
    MAX_TOKENS = 1000
