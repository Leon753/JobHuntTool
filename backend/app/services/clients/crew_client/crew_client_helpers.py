from crewai import Agent, Task
from services.tools.duckduckgo_search_tool import DuckDuckGoSearchTool
from services.tools.perplexity_search_tool import PerplexitySearchTool
from services.tools.web_scraper_tool import WebScrapperTool
from models.create_table import JobInformation
from config.crew_config import agents_config, tasks_config
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

def create_agent_from_yaml(agent_name: str, tools:list=None, max_iter = 1, **kwargs) -> Agent:
    """
    Factory method to create an Agent from a YAML config.
    Expects agents_config to be a dict with agent names as keys.
    Each agent config can include keys such as role, goal, backstory, llm, and tools.
    Additional keyword arguments (e.g., delegate=False) can be passed via kwargs.
    """

    logger.debug(f"Available agent keys: {list(agents_config.keys())}")
    config = agents_config.get(agent_name)

    if not config:
        raise ValueError(f"No configuration found for agent: {agent_name}")
    
    # If 'llm' is provided in kwargs, remove it from the config.
    if 'llm' in kwargs:
        config.pop('llm', None)

    # Create the Agent instance.
    # The Agent constructor accepts a config dict, a verbosity flag, and an optional list of tools.
    # The tools are passed as a list of Tool instances.
    agent_params = {
        "config": config,
        "verbose": True,
        "max_iter": max_iter,
    }
    # Add tools if provided.
    if tools is not None:
        agent_params["tools"] = tools

    # Merge any additional kwargs.
    agent_params.update(kwargs)
    return Agent(**agent_params)

def create_task_from_yaml(task_name: str, agent:Agent, **kwargs) -> Task:
    """
    Factory method to create a Task from a YAML config.
    Expects tasks_config to be a dict with task names as keys.
    If the task configuration contains an "agent" key,
    the task's agent will be created via create_agent_from_yaml.
    """
    task_cfg = tasks_config.get(task_name)
    if not task_cfg:
        raise ValueError(f"No configuration found for task: {task_name}")
    
    
    task_params = {
        "config": task_cfg,
        "description": task_cfg['description'],
        "expected_output": task_cfg['expected_output'],
        "agent": agent,
    }
    
    # Merge any additional kwargs.
    task_params.update(kwargs)
    return Task(**task_params)


    

    

    




