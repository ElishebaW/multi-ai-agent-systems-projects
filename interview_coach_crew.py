
import os
from crewai import Agent, Task, Crew, LLM
from tools.web_scraper import WebScraperTool

os.environ["SERPER_API_KEY"] = os.getenv('SERPER_API_KEY')
os.environ["OPENAI_API_KEY"] = "none"  # This tells CrewAI not to use OpenAI
os.environ["LOCAL_API_KEY"] = "true"

# Create the tool instance
web_scraper_tool = WebScraperTool(web_scraper_tool="https://www.hellointerview.com/learn/code")

model_name = os.environ.get("OLLAMA_MODEL", "ollama/llama2")
base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

llm=LLM(model=model_name, base_url=base_url)

# Create Agents
senior_researcher = Agent(
    role="Senior Researcher",
    goal="Gather the best interview preparation strategies for MAANG jobs.",
    backstory="Expert in coding platforms, researching the most effective study methods.",
    llm=llm,
    verbose=True,
    tools=[web_scraper_tool]
)

junior_coach = Agent(
    role="Junior Interview Coach",
    goal="Track my daily coding progress.",
    verbose = True,
    llm=llm,
    backstory="A strict but encouraging guide ensuring steady progress."
)

senior_coach = Agent(
    role="Senior Interview Coach",
    goal="Generate a structured daily interview preparation plan.",
    verbose = True,
    llm=llm,
    backstory="An experienced interview mentor optimizing study plans based on research and progress tracking."
)

# Create Tasks
research_task = Task(
    description="Gather data from NeetCode.io, LeetCode.io, CodeSignal.com, and HackerRank.com.",
    expected_output="A list of recommended exercises, study resources, and strategies.",
    output_file="interview_prep_resources_output.txt",
    agent=senior_researcher
)

track_progress_task = Task(
    description="Ask if the candidate completed medium questions in 25 minutes and easy questions in 15 minutes.",
    expected_output="A report on whether the candidate met their daily targets.",
    output_file="interview_progress_output.txt",
    agent=junior_coach
)

generate_study_plan_task = Task(
    description="Use research and progress tracking to create a detailed study plan.",
    expected_output="A structured daily plan balancing exercises, study materials, and improvement areas.",
    output_file="interview_study_plan_output.txt",
    context=[research_task, track_progress_task],
    agent=senior_coach
)

# Assemble Crew
interview_coach_crew = Crew(
    agents=[senior_researcher, junior_coach, senior_coach],
    tasks=[research_task, track_progress_task, generate_study_plan_task],
   process_inputs=False  # Tasks are completed in order
)

# Run Crew
 

try:
    # Execute the crew
    result =interview_coach_crew.kickoff()
    print(result)
except Exception as e:
    print(f"Error executing crew: {str(e)}")
