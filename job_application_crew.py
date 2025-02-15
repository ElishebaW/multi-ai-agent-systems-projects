#!/usr/bin/env python
# coding: utf-8

import warnings
import os


from crewai import Agent, Task, Crew, LLM
from crewai_tools import FileReadTool, ScrapeWebsiteTool, MDXSearchTool, SerperDevTool

warnings.filterwarnings("ignore")


# Set environment variables
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["OPENAI_API_KEY"] = "none"  # This tells CrewAI not to use OpenAI
os.environ["LOCAL_API_KEY"] = "true"

llm = LLM(model="ollama/llama2", base_url="http://localhost:11434")
# Initialize tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool(
    website_url="https://www.eventbritecareers.com/jobs/senior-software-engineer-innovation-remote-united-states"
)
read_resume = FileReadTool(file_path="./elisheba_anderson_resume_2025.pdf")
semantic_search_resume = MDXSearchTool(mdx="./elisheba_anderson_resume_2025.pdf")

# Get LLM instance

# Define all agents
researcher = Agent(
    role="Tech Job Researcher",
    goal="Make sure to do amazing analysis on job posting to help job applicants",
    tools=[scrape_tool, search_tool],
    verbose=True,
    llm=llm,
    backstory=(
        "As a Job Researcher, your prowess in navigating and extracting critical "
        "information from job postings is unmatched. Your skills help pinpoint the necessary "
        "qualifications and skills sought by employers, forming the foundation for "
        "effective application tailoring."
    ),
)

profiler = Agent(
    role="Personal Profiler for Engineers",
    goal="Do incredible research on job applicants to help them stand out in the job market",
    tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
    verbose=True,
    llm=llm,
    backstory=(
        "Equipped with analytical prowess, you dissect and synthesize information "
        "from diverse sources to craft comprehensive personal and professional profiles, "
        "laying the groundwork for personalized resume enhancements."
    ),
)

resume_strategist = Agent(
    role="Resume Strategist for Engineers",
    goal="Find all the best ways to make a resume stand out in the job market.",
    tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
    verbose=True,
    llm=llm,
    backstory=(
        "With a strategic mind and an eye for detail, you excel at refining resumes "
        "to highlight the most relevant skills and experiences, ensuring they "
        "resonate perfectly with the job's requirements."
    ),
)

interview_preparer = Agent(
    role="Engineering Interview Preparer",
    goal="Create interview questions and talking points based on the resume and job requirements",
    tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
    verbose=True,
    llm=llm,
    backstory=(
        "Your role is crucial in anticipating the dynamics of interviews. With your "
        "ability to formulate key questions and talking points, you prepare candidates "
        "for success, ensuring they can confidently address all aspects of the job "
        "they are applying for."
    ),
)

# Define all tasks
research_task = Task(
    description=(
        "Analyze the job posting URL provided ({job_posting_url}) "
        "to extract key skills, experiences, and qualifications required. "
        "Use the tools to gather content and identify and categorize the requirements."
    ),
    expected_output=(
        "A structured list of job requirements, including necessary "
        "skills, qualifications, and experiences."
    ),
    agent=researcher,
    async_execution=True,
)

profile_task = Task(
    description=(
        "Compile a detailed personal and professional profile using the  "
        " personal write-up ({personal_writeup}). "
        "Utilize tools to extract and synthesize information from these sources."
    ),
    expected_output=(
        "A comprehensive profile document that includes skills, project experiences, "
        "contributions, interests, and communication style."
    ),
    agent=profiler,
    async_execution=True,
)

resume_strategy_task = Task(
    description=(
        "Using the profile and job requirements obtained from previous tasks, "
        "tailor the resume to highlight the most relevant areas. Employ tools "
        "to adjust and enhance the resume content. Make sure this is the best "
        "resume even but don't make up any information. Update every section, "
        "including the initial summary, work experience, skills, and education. "
        "All to better reflect the candidates abilities and how it matches the job posting."
    ),
    expected_output=(
        "An updated resume that effectively highlights the candidate's "
        "qualifications and experiences relevant to the job."
    ),
    output_file="tailored_resume.pdf",
    context=[research_task, profile_task],
    agent=resume_strategist,
)

interview_preparation_task = Task(
    description=(
        "Create a set of potential interview questions and talking points based "
        "on the tailored resume and job requirements. Utilize tools to generate "
        "relevant questions and discussion points. Make sure to use these questions "
        "and talking points to help the candidate highlight the main points of the "
        "resume and how it matches the job posting."
    ),
    expected_output=(
        "A document containing key questions and talking points that the candidate "
        "should prepare for the initial interview."
    ),
    output_file="interview_materials.md",
    context=[research_task, profile_task, resume_strategy_task],
    agent=interview_preparer,
)

# Create and configure the crew
job_application_crew = Crew(
    agents=[researcher, profiler, resume_strategist, interview_preparer],
    tasks=[
        research_task,
        profile_task,
        resume_strategy_task,
        interview_preparation_task,
    ],
    verbose=True,
    process_inputs=False,
)

if __name__ == "__main__":
    # Your inputs
    job_application_inputs = {
        "job_posting_url": "https://www.eventbritecareers.com/jobs/senior-software-engineer-innovation-remote-united-states",
        "personal_writeup": """Elisheba is a Senior Software Engineer with 6+ years of experience who crafts software to tackle complex challenges. I own
    the SDLC for projects, architect scalable solutions in distributed systems, and ensure security. With a track record of
    driving revenue growth and operational efficiency, I thrive in collaborative environments where continuous learning
    is key.""",
    }

    try:
        # Execute the crew
        result = job_application_crew.kickoff(inputs=job_application_inputs)
        print(result)
    except Exception as e:
        print(f"Error executing crew: {str(e)}")
