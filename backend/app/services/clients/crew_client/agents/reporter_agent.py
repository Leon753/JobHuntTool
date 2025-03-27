from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai import LLM
from config.logger import logger
from services.clients.crew_client.crew_client_helpers import * 
from config.keys import GPT4_KEY
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
        agent = create_agent_from_yaml("reporting_analyst",tools=None, max_iter=1)
        agent.llm = LLM(
            model="azure/gpt-4-32k",
            api_version="2025-01-01-preview",
            base_url="https://aminm-m4mihuzx-francecentral.cognitiveservices.azure.com",
            api_key=GPT4_KEY
        )
        return agent
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