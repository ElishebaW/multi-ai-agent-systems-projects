import os
from crewai import Agent, Task, Crew, LLM

# Set environment variables to force local LLM usage
os.environ["OPENAI_API_KEY"] = "none"  # Disables OpenAI usage
os.environ["LOCAL_API_KEY"] = "true"  # Enables local LLMs

# Define local models
llama_llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
mistral_llm = LLM(model="ollama/mistral", base_url="http://localhost:11434")
qwen_llm = LLM(model="ollama/qwen:7b", base_url="http://localhost:11434")

# Define agents, each using a different local LLM
llama_agent = Agent(
    role="Senior Java Engineer - Llama",
    goal="Explain Dijkstra’s algorithm in a way that a beginner can understand, with a step-by-step breakdown and a code example in Java using Llama 3.2.",
    backstory="A expert Java engineer with 30 years of experience in algorithmic problem-solving, utilizing Llama 3.2 to craft efficient and optimized solutions.",
    verbose=True,
    llm=llama_llm,
)

mistral_agent = Agent(
    role="Senior Java Engineer - Mistral",
    goal="Explain Dijkstra’s algorithm in a way that a beginner can understand, with a step-by-step breakdown and a code example in Java using Mistral.",
    backstory="A expert Java engineer with 30 years of experience in algorithmic problem-solving, utilizing Mistral to craft efficient and optimized solutions.",
    verbose=True,
    llm=mistral_llm,
)

qwen_agent = Agent(
    role="Senior Java Engineer - Qwen",
    goal="Explain Dijkstra’s algorithm in a way that a beginner can understand, with a step-by-step breakdown and a code example in Java using Qwen-7B.",
    backstory="A expert Java engineer with 30 years of experience in algorithmic problem-solving, utilizing Qwen-7B to craft efficient and optimized solutions.",
    verbose=True,
    llm=qwen_llm,
)

# Define the task for all agents
fib_task_llama = Task(
    description="Explain Dijkstra’s algorithm in a way that a beginner can understand, with a step-by-step breakdown and a code example in Java.",
    expected_output="A step-by-step breakdown of Dijkstra's Algorithm and a code example in Java.",
    output_file="llm_performance-algo.md",
    agent=llama_agent,
)

fib_task_mistral = Task(
    description="Explain Dijkstra’s algorithm in a way that a beginner can understand, with a step-by-step breakdown and a code example in Java.",
    expected_output="A step-by-step breakdown of Dijkstra's Algorithm and a code example in Java.",
    output_file="llm_performanc-algo.md",
    agent=mistral_agent,
)
fib_task_qwen = Task(
    description="Explain Dijkstra’s algorithm in a way that a beginner can understand, with a step-by-step breakdown and a code example in Java.",
    expected_output="A step-by-step breakdown of Dijkstra's Algorithm and a code example in Java.",
    output_file="llm_performance-algo.md",
    agent=qwen_agent,
)

# Create a crew to execute the tasks in parallel
crew = Crew(
    agents=[llama_agent, mistral_agent, qwen_agent],
    tasks=[fib_task_llama, fib_task_mistral, fib_task_qwen],
    # process=Process.parallel,  # Run all agents in parallel
)

results = crew.kickoff()
