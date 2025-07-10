"""Database module for storing and retrieving plans."""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import json

DB_PATH = Path("plans.db")

def init_db():
    """Initialize the SQLite database with required tables."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Create plans table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            date TEXT PRIMARY KEY,
            schedule TEXT NOT NULL,
            reasoning TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

def save_plan(schedule: str, reasoning: str, plan_date: Optional[str] = None) -> bool:
    """
    Save a plan to the database.
    
    Args:
        schedule: The formatted schedule
        reasoning: The reasoning behind the schedule
        plan_date: Optional date string in any format. Uses today if None.
                  Will be converted to YYYY-MM-DD format.
                  
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Convert input date to YYYY-MM-DD format
        if plan_date is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                # Handle various date formats
                date_obj = datetime.strptime(plan_date, "%Y-%m-%d")
            except ValueError:
                try:
                    date_obj = datetime.strptime(plan_date, "%Y/%m/%d")
                except ValueError:
                    # If we can't parse it, try to extract date from string
                    try:
                        date_obj = datetime.strptime(plan_date.split()[0], "%Y-%m-%d")
                    except:
                        print(f"Warning: Could not parse date: {plan_date}")
                        date_obj = datetime.now()
            date_str = date_obj.strftime("%Y-%m-%d")
        
        print(f"\n🔍 Debug - Saving plan:")
        print(f"  Date: {date_str}")
        print(f"  Schedule length: {len(schedule)}")
        print(f"  Reasoning length: {len(reasoning)}")
        
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO plans (date, schedule, reasoning)
                VALUES (?, ?, ?)
                """,
                (date_str, schedule, reasoning)
            )
            conn.commit()
            print("✅ Plan saved successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error saving plan: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_plan(date: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Retrieve a plan from the database.
    
    Args:
        date: Optional date string in any format. Uses today if None.
              Will be converted to YYYY-MM-DD format for comparison.
              
    Returns:
        Dict containing 'schedule' and 'reasoning' if found, None otherwise
    """
    print("\n🔍 Debug - get_plan:")
    print(f"  Input date: {date}")
    
    try:
        # Convert input date to datetime object and then to YYYY-MM-DD format
        if date is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
            print("  Using today's date:", date_str)
        else:
            original_date = date
            try:
                # Handle various date formats
                date_obj = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                try:
                    date_obj = datetime.strptime(date, "%Y/%m/%d")
                except ValueError:
                    # If we can't parse it, try to extract date from string
                    try:
                        date_obj = datetime.strptime(date.split()[0], "%Y-%m-%d")
                    except:
                        print(f"  Warning: Could not parse date: {date}")
                        date_obj = datetime.now()
            date_str = date_obj.strftime("%Y-%m-%d")
            print(f"  Formatted date: {date_str}")
        
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # First try exact match with formatted date
            print(f"  Querying for exact date: {date_str}")
            cursor.execute(
                "SELECT date, schedule, reasoning FROM plans WHERE date = ?",
                (date_str,)
            )
            row = cursor.fetchone()
            
            if not row and date is not None and date_str != date:
                # Try with the original date string if different
                print(f"  No exact match, trying original date format: {date}")
                cursor.execute(
                    "SELECT date, schedule, reasoning FROM plans WHERE date = ?",
                    (date,)
                )
                row = cursor.fetchone()
            
            if not row:
                # Try a LIKE query to see if there are any similar dates
                print(f"  No exact matches, checking for similar dates...")
                cursor.execute(
                    "SELECT date, schedule, reasoning FROM plans WHERE date LIKE ?",
                    (f"%{date_str}%",)
                )
                row = cursor.fetchone()
                if row:
                    print(f"  Found similar date: {row['date']}")
            
            if row:
                print(f"✅ Found plan for date: {row['date']}")
                return dict(row)
            else:
                print("❌ No matching plan found")
                
    except Exception as e:
        print(f"❌ Error retrieving plan: {e}")
        import traceback
        traceback.print_exc()
    
    return None
    
def get_recent_plans(limit: int = 5) -> list:
    """
    Retrieve recent plans from the database.
    
    Args:
        limit: Maximum number of plans to return
        
    Returns:
        List of recent plans with date, schedule, and reasoning
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT date, schedule, reasoning 
                FROM plans 
                ORDER BY date DESC 
                LIMIT ?
                """,
                (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

# Initialize the database when module is imported
init_db()
