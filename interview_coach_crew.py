
import os
from tabnanny import verbose
from crewai import Agent, Task, Crew
from tools.web_scraper import WebScraperTool

# Create the tool instance
web_scraper = WebScraperTool()

# Load API Keys if required (for external tools)
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Create Agents
senior_researcher = Agent(
    role="Senior Researcher",
    goal="Gather the best interview preparation strategies for MAANG jobs.",
    backstory="Expert in coding platforms, researching the most effective study methods.",
    verbose=True,
    tools=[WebScraperTool()]
)

junior_coach = Agent(
    role="Junior Interview Coach",
    goal="Track the candidate’s daily coding progress.",
    verbose = True,
    backstory="A strict but encouraging guide ensuring steady progress."
)

senior_coach = Agent(
    role="Senior Interview Coach",
    goal="Generate a structured daily interview preparation plan.",
    verbose = True,
    backstory="An experienced interview mentor optimizing study plans based on research and progress tracking."
)

# Create Tasks
research_task = Task(
    description="Gather data from NeetCode.io, LeetCode.io, CodeSignal.com, and HackerRank.com.",
    expected_output="A list of recommended exercises, study resources, and strategies.",
    agent=senior_researcher
)

track_progress_task = Task(
    description="Ask if the candidate completed medium questions in 25 minutes and easy questions in 15 minutes.",
    expected_output="A report on whether the candidate met their daily targets.",
    agent=junior_coach
)

generate_study_plan_task = Task(
    description="Use research and progress tracking to create a detailed study plan.",
    expected_output="A structured daily plan balancing exercises, study materials, and improvement areas.",
    agent=senior_coach
)

# Assemble Crew
crew = Crew(
    agents=[senior_researcher, junior_coach, senior_coach],
    tasks=[research_task, track_progress_task, generate_study_plan_task],
    process=Process.sequential  # Tasks are completed in order
)

# Run Crew
results = crew.kickoff()
print(results)
