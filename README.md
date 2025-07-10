# AI Daily Planner

An intelligent productivity assistant that generates optimal daily schedules using AI. Input your tasks, and the agent will create a smart, time-blocked schedule that's both realistic and productive.

## 🚀 Features

- **AI-Powered Scheduling**: Uses GPT-4o to create intelligent, time-blocked schedules
- **Task Prioritization**: Automatically prioritizes tasks based on importance and deadlines
- **Smart Time Allocation**: Considers task duration, energy levels, and productivity patterns
- **Clear Rationale**: Provides explanations for scheduling decisions
- **Easy to Use**: Simple command-line interface with sensible defaults

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

Run the planner with example tasks:
```bash
python main.py
```

Or provide your own tasks:
```bash
python main.py --tasks "Finish project report, Team meeting, Code review, Lunch break"
```

## 📁 Project Structure

```
ai_daily_planner/
├── main.py                # Main entry point
├── planner/
│   ├── agent.py          # LangChain logic for schedule generation
│   └── prompt.py         # Prompt templates and system messages
├── config/
│   └── config.py         # Configuration and environment setup
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## 🤖 How It Works

The AI Daily Planner uses LangChain and OpenAI's GPT-4o to:
1. Process your list of tasks
2. Consider priorities, durations, and deadlines
3. Create an optimal time-blocked schedule
4. Provide a rationale for the scheduling decisions

## 📝 Example Output

```
📅 YOUR OPTIMAL SCHEDULE
==================================================
09:00 - 10:00 - Team standup meeting (Priority: High, Duration: 60 min)
  • Description: Daily sync with the team
  • Rationale: Starting the day with alignment helps set priorities

10:00 - 11:30 - Work on feature X implementation (Priority: High, Duration: 90 min)
  • Description: Core development work
  • Rationale: Morning hours are best for deep work

...

💡 Schedule Rationale:
I've scheduled the most important tasks in the morning when energy levels are typically highest...
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
