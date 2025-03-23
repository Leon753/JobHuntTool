from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from services.tools.duckduckgo_search_tool import DuckDuckGoSearchTool
from services.tools.perplexity_search_tool import PerplexitySearchTool
from services.tools.web_scraper_tool import WebScrapperTool
from models.create_table import JobInformation
import os
import yaml
from config.keys import *
from config.logger import logger


Tools = {
    "perplexity_search_tool" : PerplexitySearchTool(),
    "duck_search_tool": DuckDuckGoSearchTool(),
    "webscrapper": WebScrapperTool()

}
OUTPUT_JSON = {
    "JobInformation": JobInformation
}
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
def create_agent_from_yaml(agent_name: str, tools:list=None) -> Agent:
    """
    Factory method to create an Agent from a YAML config.
    Expects agents_config to be a dict with agent names as keys.
    Each agent config can include keys such as role, goal, backstory, llm, and tools.
    """

    logger.debug(f"Available agent keys: {list(agents_config.keys())}")
    config = agents_config.get(agent_name)

    if not config:
        raise ValueError(f"No configuration found for agent: {agent_name}")
   
    # Create the Agent instance.
    # The Agent constructor accepts a config dict, a verbosity flag, and an optional list of tools.
    # print("config {agent_name}" , config)
    if tools is None:
        return Agent(
            config=config,
            verbose=True,
            max_iter=2,
        )
    return Agent(
            config=config,
            verbose=True,
            max_iter=1,
            tools=tools
        )

def create_task_from_yaml(task_name: str) -> Task:
    """
    Factory method to create a Task from a YAML config.
    Expects tasks_config to be a dict with task names as keys.
    If the task configuration contains an "agent" key,
    the task's agent will be created via create_agent_from_yaml.
    """
    task_cfg = tasks_config.get(task_name)
    if not task_cfg:
        raise ValueError(f"No configuration found for task: {task_name}")
    output_json = None
    if task_cfg.get("output_json", "") != "":
        output_json = OUTPUT_JSON[task_cfg.get("output_json")]
    agent_instance = None
    if "agent" in task_cfg:
        agent_instance = create_agent_from_yaml(task_cfg["agent"])
    return Task(
        config=task_cfg,
        description=task_cfg['description'],
        expected_output=task_cfg['expected_output'],
        agent=agent_instance,
        output_json=output_json
    )

@CrewBase
class TableMakerCrew():
    @before_kickoff
    def before_kickoff_function(self, inputs):
        logger.info(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed
    
    @after_kickoff
    def after_kickoff_function(self, result):
        logger.info(f"After kickoff function with result: {result}")
        return result # You can return the result or modify it as needed
    
    @agent
    def company_corporate_researcher(self) -> Agent:
        return create_agent_from_yaml("company_corporate_researcher", [Tools["perplexity_search_tool"]])
      # @agent
    @task
    def company_corporate_research_task(self) -> Task:
        return Task(
            config=tasks_config['company_corporate_research_task'],
            description=tasks_config['company_corporate_research_task']['description'],
            expected_output=tasks_config['company_corporate_research_task']['expected_output'],
            agent=self.company_corporate_researcher()
        )
    
    
    @agent
    def mission_vision_researcher(self) -> Agent:
        return create_agent_from_yaml("mission_vision_researcher", [Tools["perplexity_search_tool"]])
    @task
    def mission_vision_researcher_task(self) -> Task:
        return Task(
            description=tasks_config['mission_vision_research_task']['description'],
            expected_output=tasks_config['mission_vision_research_task']['expected_output'],
            agent=self.mission_vision_researcher()
        )
    @agent
    def financial_market_researcher(self) -> Agent:
        return create_agent_from_yaml("financial_market_researcher", [Tools["perplexity_search_tool"]])

    @task
    def financial_market_researcher_task(self) -> Task:
        return Task(
            config=tasks_config['financial_market_research_task'],
            description=tasks_config['financial_market_research_task']['description'],
            expected_output=tasks_config['financial_market_research_task']['expected_output'],
            agent=self.financial_market_researcher()
        )
    @agent 
    def job_role_researcher(self) -> Agent:
        return create_agent_from_yaml("job_role_researcher", [Tools["perplexity_search_tool"]])
    @task
    def job_role_researcher_task(self) -> Task:
        return Task(
            config=tasks_config['job_role_research_task'],
            description=tasks_config['job_role_research_task']['description'],
            expected_output=tasks_config['job_role_research_task']['expected_output'],
            agent=self.job_role_researcher()
        )
    @agent
    def compensation_career_culture_researcher(self) -> Agent:
        return create_agent_from_yaml("compensation_career_culture_researcher", [Tools["perplexity_search_tool"]])
    @task
    def compensation_career_culture_researcher_task(self) -> Task:
        return Task(
            config=tasks_config['compensation_career_culture_research_task'],
            description=tasks_config['compensation_career_culture_research_task']['description'],
            expected_output=tasks_config['compensation_career_culture_research_task']['expected_output'],
            agent=self.compensation_career_culture_researcher()
        )
    @agent
    def reporting_analyst(self) -> Agent:
        return create_agent_from_yaml("reporting_analyst")
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
        # print(self.agents)
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
    
@CrewBase
class CompanyResearcher():
    @before_kickoff
    def before_kickoff_function(self, inputs):
        logger.info(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed
    
    @after_kickoff
    def after_kickoff_function(self, result):
        logger.info(f"After kickoff function with result: {result}")
        return result # You can return the result or modify it as needed
    
    @agent
    def company_corporate_researcher(self) -> Agent:
        return create_agent_from_yaml("company_corporate_researcher",[Tools["perplexity_search_tool"]])
      # @agent
    @task
    def company_corporate_research_task(self) -> Task:
        return Task(
            config=tasks_config['company_corporate_research_task'],
            description=tasks_config['company_corporate_research_task']['description'],
            expected_output=tasks_config['company_corporate_research_task']['expected_output'],
            agent=self.company_corporate_researcher()
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        # print(self.agents)
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
    
@CrewBase
class MissionResearcher():
    @before_kickoff
    def before_kickoff_function(self, inputs):
        logger.info(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed
    
    @after_kickoff
    def after_kickoff_function(self, result):
        logger.info(f"After kickoff function with result: {result}")
        return result # You can return the result or modify it as needed
    
    @agent
    def mission_vision_researcher(self) -> Agent:
        print("we are in mission ")
        return create_agent_from_yaml("mission_vision_researcher", [Tools["perplexity_search_tool"]])
    @task
    def mission_vision_researcher_task(self) -> Task:
        return Task(
            description=tasks_config['mission_vision_research_task']['description'],
            expected_output=tasks_config['mission_vision_research_task']['expected_output'],
            agent=self.mission_vision_researcher()
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        # print(self.agents)
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
    
@CrewBase
class FinancialResearcher():
    @before_kickoff
    def before_kickoff_function(self, inputs):
        logger.info(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed
    
    @after_kickoff
    def after_kickoff_function(self, result):
        logger.info(f"After kickoff function with result: {result}")
        return result # You can return the result or modify it as needed
    

    @agent
    def financial_market_researcher(self) -> Agent:
        return create_agent_from_yaml("financial_market_researcher", [Tools["perplexity_search_tool"]])
        
    @task
    def financial_market_researcher_task(self) -> Task:
        return Task(
            config=tasks_config['financial_market_research_task'],
            description=tasks_config['financial_market_research_task']['description'],
            expected_output=tasks_config['financial_market_research_task']['expected_output'],
            agent=self.financial_market_researcher()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        # print(self.agents)
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
    
@CrewBase
class JobRoleResearcher():
    @before_kickoff
    def before_kickoff_function(self, inputs):
        logger.info(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed
    
    @after_kickoff
    def after_kickoff_function(self, result):
        logger.info(f"After kickoff function with result: {result}")
        return result # You can return the result or modify it as needed
    
    @agent 
    def job_role_researcher(self) -> Agent:
        return create_agent_from_yaml("job_role_researcher", [Tools["perplexity_search_tool"]])
    @task
    def job_role_researcher_task(self) -> Task:
        return Task(
            config=tasks_config['job_role_research_task'],
            description=tasks_config['job_role_research_task']['description'],
            expected_output=tasks_config['job_role_research_task']['expected_output'],
            agent=self.job_role_researcher()
        )
    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        # print(self.agents)
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
@CrewBase
class CompensationAndCultureResearcher():
    @before_kickoff
    def before_kickoff_function(self, inputs):
        logger.info(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed
    
    @after_kickoff
    def after_kickoff_function(self, result):
        logger.info(f"After kickoff function with result: {result}")
        return result # You can return the result or modify it as needed
    
   
    @agent
    def compensation_career_culture_researcher(self) -> Agent:
        return create_agent_from_yaml("compensation_career_culture_researcher", [Tools["perplexity_search_tool"]])
    @task
    def compensation_career_culture_researcher_task(self) -> Task:
        return Task(
            config=tasks_config['compensation_career_culture_research_task'],
            description=tasks_config['compensation_career_culture_research_task']['description'],
            expected_output=tasks_config['compensation_career_culture_research_task']['expected_output'],
            agent=self.compensation_career_culture_researcher()
        )

  
    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        # print(self.agents)
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
    
@CrewBase
class Reporter():
    @before_kickoff
    def before_kickoff_function(self, inputs):
        logger.info(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed
    
    @after_kickoff
    def after_kickoff_function(self, result):
        logger.info(f"After kickoff function with result: {result}")
        return result # You can return the result or modify it as needed
    
    
    @agent
    def reporting_analyst(self) -> Agent:
        return create_agent_from_yaml("reporting_analyst",tools=None)
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
        # print(self.agents)
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )