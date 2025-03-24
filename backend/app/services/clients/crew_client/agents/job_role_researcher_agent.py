from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from config.logger import logger
from services.clients.crew_client.crew_client_helpers import * 

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