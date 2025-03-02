from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from langchain_community.tools import DuckDuckGoSearchRun
from crewai_tools import (WebsiteSearchTool, FileReadTool)
from services.tools.PerplexitySearchTool import PerplexitySearchTool

from dotenv import load_dotenv
import os
import yaml
import sys
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = os.getenv("PERPLEXITY_API_URL")
OPENAI_GPT4_KEY = os.getenv("AZURE_API_KEY")
ENDPOINT_OPENAI_GPT4 = os.getenv("AZURE_API_BASE")
TEXT_EMBEDDINGS_API_KEY = os.getenv("TEXT_EMBEDDINGS_API_KEY")
TEXT_EMBEDDINGS_API_BASE = os.getenv("TEXT_EMBEDDINGS_API_BASE")
TEXT_EMBEDDINGS_API_VERSION = os.getenv("TEXT_EMBEDDINGS_API_VERSION")


CHAT_VERSION = "2024-08-01-preview"  # Update if needed
CHAT_DEPLOYMENT_NAME = "gpt-4o"  # Replace with your deployed model name
LLM = {
        "model": f"azure/{CHAT_DEPLOYMENT_NAME}",  # Azure OpenAI uses "deployment name"
        "api_key": OPENAI_GPT4_KEY,
        "base_url": f"{ENDPOINT_OPENAI_GPT4}/openai/deployments/{CHAT_DEPLOYMENT_NAME}/chat/completions?api-version={CHAT_VERSION}",
    }

print(OPENAI_GPT4_KEY)
config=dict(
        llm=dict(
        provider="azure_openai",
        config=dict(
            model="gpt-4o",
            api_key=OPENAI_GPT4_KEY,
            deployment_name=ENDPOINT_OPENAI_GPT4
        ),
    ),
        embedder=dict(
            provider="azure_openai",  # Options include 'openai', 'ollama', etc.
            config=dict(
                model="text-embedding-3-small",
                api_key=OPENAI_GPT4_KEY,
                deployment_name=ENDPOINT_OPENAI_GPT4
                # Additional parameters like title can be set here
            ),
        ),
    )


config = dict(
    llm=dict(
        provider="azure_openai",
        config=dict(
            model="gpt-4o",
            api_key=OPENAI_GPT4_KEY,
            deployment_name=ENDPOINT_OPENAI_GPT4
        ),
    )
)
# Define the input dictionary with the required keys
input_string = "Circle Internet Financial mission vision strategic goals, website: https://www.circle.com"
search_tool = WebsiteSearchTool(config=config)
current_dir = os.path.dirname(os.path.abspath(__file__))


# Load YAML Configuration
def load_config(file:str):
    config_path = os.path.join(current_dir, "..", "config", file)
    # Ensure the path is correct
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    with open(config_path,"r") as file:
        return yaml.safe_load(file)

agents_config = load_config("agents.yaml")
tasks_config = load_config("tasks.yaml")

print(agents_config['researcher'])
print(tasks_config['research_task'].get('config', {}))
print(tasks_config['reporting_task'].get('config', {}))

@CrewBase
class LatestAiDevelopmentCrew():
    @before_kickoff
    def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed
    
    @after_kickoff
    def after_kickoff_function(self, result):
        print(f"After kickoff function with result: {result}")
        return result # You can return the result or modify it as needed
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=agents_config['researcher'],
            verbose=True,
            tools=[search_tool],
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=agents_config['reporting_analyst'],
            verbose=True,
        )
    
    @task
    def research_task(self) -> Task:
        return Task(
            config=tasks_config['research_task'],
            description=tasks_config['research_task']['description'],
            expected_output=tasks_config['research_task']['expected_output'],
            agent=self.researcher()
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
        description=tasks_config['reporting_task']['description'],
        expected_output=tasks_config['reporting_task']['expected_output'],
        agent=self.reporting_analyst(),
        output_file='output/report.md' # This is the file that will be contain the final report.
        )
    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        return Crew(
        agents=self.agents, # Automatically created by the @agent decorator
        tasks=self.tasks, # Automatically created by the @task decorator
        process=Process.sequential,
        verbose=True,
        )