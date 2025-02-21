import os
from crewai import Agent, Task, Crew, Process, LLM

# Set environment variables to force local LLM usage
os.environ["OPENAI_API_KEY"] = "none"  # Disables OpenAI usage
os.environ["LOCAL_API_KEY"] = "true"  # Enables local LLMs

# Define local models
llama_llm = LLM(model="ollama/llama2", base_url="http://localhost:11434")
deepseek_llm = LLM(model="ollama/deepseek-r1", base_url="http://localhost:11434")
gemini_llm = LLM(model="ollama/gemini", base_url="http://localhost:11434")
qwen_llm = LLM(model="ollama/qwen-7B", base_url="http://localhost:11434")

# Define agents, each using a different local LLM
llama_agent = Agent(
    role="Java Engineer",
    goal="Generate a Fibonacci function using Llama 3.2",
    backstory="An expert Java programmer using Llama 3.2 to solve coding problems.",
    verbose=True,
    llm=llama_llm,
)

deepseek_agent = Agent(
    role="Java Engineer",
    goal="Generate a Fibonacci function using Deepseek-R1",
    backstory="An expert Java programmer using Deepseek-R1 to solve coding problems.",
    verbose=True,
    llm=deepseek_llm,
)

gemini_agent = Agent(
    role="Software Engineer",
    goal="Generate a Fibonacci function using Gemini",
    backstory="A talented software engineer utilizing Gemini for optimal Java scripts.",
    verbose=True,
    llm=gemini_llm,
)

qwen_agent = Agent(
    role="ML Researcher",
    goal="Generate a Fibonacci function using Qwen-7B",
    backstory="An ML researcher experimenting with Qwen-7B for Java programming.",
    verbose=True,
    llm=qwen_llm,
)

# Define the task for all agents
fib_task = Task(
    description="Write a short Java function that returns the Fibonacci sequence up to a given number.",
    expected_output="A Java function that computes Fibonacci numbers up to n.",
)

# Assign each agent to the task
fib_task_llama = fib_task.copy(update={"agent": llama_agent})
fib_task_deepseek = fib_task.copy(update={"agent": deepseek_agent})
fib_task_gemini = fib_task.copy(update={"agent": gemini_agent})
fib_task_qwen = fib_task.copy(update={"agent": qwen_agent})

# Create a crew to execute the tasks in parallel
crew = Crew(
    agents=[llama_agent, deepseek_agent, gemini_agent, qwen_agent],
    tasks=[fib_task_llama, fib_task_deepseek, fib_task_gemini, fib_task_qwen],
    process=Process.parallel,  # Run all agents in parallel
)

# Execute the tasks
results = crew.kickoff()

# Print results
for model, result in zip(["Llama 3.2", "Deepseek-R1", "Gemini", "Qwen-7B"], results):
    print(f"\n### Response from {model}:")
    print(result)
