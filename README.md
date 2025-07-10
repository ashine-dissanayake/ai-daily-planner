# AI Daily Planner

An intelligent productivity assistant that generates optimal daily schedules using AI. Input your tasks, and the agent will create a smart, time-blocked schedule that's both realistic and productive.

## 🚀 Features

- **AI-Powered Scheduling**: Uses GPT-4o to create intelligent, time-blocked schedules
- **Task Prioritization**: Automatically prioritizes tasks based on importance and deadlines
- **Smart Time Allocation**: Considers task duration, energy levels, and productivity patterns
- **Clear Rationale**: Provides explanations for scheduling decisions
- **Persistent Storage**: Saves plans to SQLite database for future reference
- **Markdown Export**: Exports schedules to nicely formatted Markdown files
- **Customizable Preferences**: Set work hours, break intervals, and deep work preferences
- **Plan History**: View and manage previous schedules
- **Interactive Task Input**: Simple command-line interface with task metadata support

## 🛠 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-daily-planner.git
   cd ai-daily-planner
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🚦 Quick Start

### Basic Usage

Run the planner with interactive task input:
```bash
python3 main.py
```

### Command Line Options

- **View today's plan**:
  ```bash
  python3 main.py --view
  ```

- **View recent plans** (last 3 by default):
  ```bash
  python3 main.py --recent
  ```
  View a specific number of recent plans:
  ```bash
  python3 main.py --recent 5
  ```

- **View plan for a specific date**:
  ```bash
  python3 main.py --date 2025-07-10
  ```

- **Edit preferences**:
  ```bash
  python3 main.py --prefs
  ```

### Interactive Task Input

When running without arguments, the planner will prompt you to enter tasks one by line. For each task, you can specify:
- Task name (required)
- Priority (High/Medium/Low)
- Duration (in minutes)
- Deadline (HH:MM)

Example task entries:
```
Write project report priority=High duration=120 due=18:00
Team standup duration=30
Lunch break duration=60
```

## 📁 Project Structure

```
ai-daily-planner/
├── main.py                # Main entry point and CLI interface
├── planner/
│   ├── agent.py           # LangChain logic for schedule generation
│   ├── prompt.py          # Prompt templates and system messages
│   └── preferences.py     # User preferences and settings
├── io_modules/
│   ├── input_parser.py    # Task input parsing and validation
│   └── output_writer.py   # Markdown export functionality
├── memory/
│   └── db.py             # SQLite database operations
├── config/
│   └── config.py         # Configuration and environment setup
├── DailyPlans/           # Generated schedule files
├── .env                  # Environment variables
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## 🤖 How It Works

The AI Daily Planner is a smart scheduling assistant that helps you organize your day efficiently. Here's how it works:

1. **Task Input**:
   - Enter tasks interactively or load from a saved plan
   - For each task, specify details like priority, duration, and deadline
   
2. **AI-Powered Scheduling**:
   - Uses LangChain with GPT-4o to analyze your tasks
   - Considers task priorities, durations, and deadlines
   - Takes into account your work hours and preferences
   - Creates a realistic, time-blocked schedule
   
3. **Smart Features**:
   - **Time Blocking**: Groups related tasks and allocates appropriate time slots
   - **Energy Management**: Schedules demanding tasks during peak productivity hours
   - **Break Optimization**: Includes breaks between tasks for better focus
   - **Context Awareness**: Considers task dependencies and logical ordering
   
4. **Output**:
   - Displays the schedule in an easy-to-read format
   - Provides rationale for scheduling decisions
   - Saves the plan to the database for future reference
   - Exports to markdown for easy sharing and printing

## 📝 Example Output

### Command Line Interface
```
$ python3 main.py

🤖 Welcome to AI Daily Planner!

📝 Enter your tasks (one per line, empty line to finish):
• Write project report priority=High duration=120 due=18:00
• Team standup duration=30
• Code review PR #42 priority=High duration=45
• Lunch break duration=45
• Work on feature X implementation duration=90
• 
📋 Tasks to schedule:
1. Write project report | Priority: High | Duration: 120 min | Due: 18:00
2. Team standup | Duration: 30 min
3. Code review PR #42 | Priority: High | Duration: 45 min
4. Lunch break | Duration: 45 min
5. Work on feature X implementation | Duration: 90 min

⏰ Current time: Thursday, July 10, 2025 09:00 AM
⏳ Generating your optimal schedule...
```

### Generated Schedule
```
📅 YOUR OPTIMAL SCHEDULE
==================================================
09:00 - 09:30  Team Standup
  • Duration: 30 min | Priority: Normal
  • Description: Daily team synchronization

09:30 - 11:30  Write Project Report
  • Duration: 120 min | Priority: High | Due: 18:00
  • Description: Complete the quarterly report with updated metrics
  • Rationale: High priority task with deadline today

11:30 - 12:15  Code Review PR #42
  • Duration: 45 min | Priority: High
  • Description: Review pull request for new authentication flow
  • Rationale: Important task before lunch, keeps code review momentum

12:15 - 13:00  Lunch Break
  • Duration: 45 min
  • Rationale: Midday break for rest and meal

13:00 - 14:30  Work on Feature X Implementation
  • Duration: 90 min | Priority: Normal
  • Description: Implement new user dashboard components
  • Rationale: After-lunch focus period for development work

💡 Schedule Rationale:
I've scheduled your highest priority tasks in the morning when cognitive resources are typically at their peak. The project report is scheduled first as it has a hard deadline today. The code review is placed before lunch to ensure it gets proper attention. The afternoon is reserved for focused development work on the feature implementation. Breaks are included to maintain productivity throughout the day.

✅ Plan saved and exported to DailyPlans/2025-07-10.md
```

## 📈 Future Enhancements

- [ ] Google Calendar integration
- [ ] Vector memory for personalized scheduling
- [ ] Streamlit web interface
- [ ] Recurring task support
- [ ] Time tracking and analytics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
