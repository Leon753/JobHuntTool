from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from services.tools.duckduckgo_search_tool import DuckDuckGoSearchTool
from services.tools.perplexity_search_tool import PerplexitySearchTool
from services.tools.web_scraper_tool import WebScrapperTool
from models.create_table import JobInformation
import os
import yaml
from config.keys import *

duck_search_tool = DuckDuckGoSearchTool()
perplexity_search_tool = PerplexitySearchTool()


webscrapper = WebScrapperTool()
#TODO Need to delete this lines



current_dir = os.path.dirname(os.path.abspath(__file__))
# Load YAML Configuration
def load_config(file:str):
    config_path = os.path.join(current_dir, "..","..", "config", file)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    with open(config_path,"r") as file:
        return yaml.safe_load(file)

agents_config = load_config("agents.yaml")
tasks_config = load_config("tasks.yaml")


config = dict(
    llm=dict(
        provider="azure_openai",
        config=dict(
            model="gpt-4o",
        ),
    ),
    embedder=dict(
        provider="azure_openai",
        config=dict(
            model="text-embedding-3-small",
            deployment_name="text-embedding-3-small",
            api_base = TEXT_EMBEDDINGS_API_BASE,
            api_key=TEXT_EMBEDDINGS_API_KEY,
        ),
    )
)

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
            tools=[duck_search_tool],
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
            output_json=JobInformation,
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