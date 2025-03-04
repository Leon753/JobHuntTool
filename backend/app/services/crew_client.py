from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai.memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.storage.rag_storage import RAGStorage
from services.tools.PerplexitySearchTool import PerplexitySearchTool
from models.create_table import JobInformation
import os
import yaml
from config.keys import *


search_tool = PerplexitySearchTool()
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load YAML Configuration
def load_config(file:str):
    config_path = os.path.join(current_dir, "..", "config", file)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    with open(config_path,"r") as file:
        return yaml.safe_load(file)

agents_config = load_config("agents.yaml")
tasks_config = load_config("tasks.yaml")

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
            #tools=[search_tool],
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
            output_file='output/report.md' # This is the file that will be contain the final report.
        )
    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
        )
            