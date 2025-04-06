from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from config.logger import logger
from services.clients.crew_client.crew_client_helpers import * 
from crewai import LLM
from config.keys import OPENAI_GPT4_KEY
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
    def compensation_career_culture_researcher(self) -> Agent:
        return create_agent_from_yaml("compensation_career_culture_researcher", [Tools["perplexity_search_tool"]])
    @task
    def compensation_career_culture_researcher_task(self) -> Task:
        return create_task_from_yaml("compensation_career_culture_research_task", agent=self.compensation_career_culture_researcher())
    
    @agent 
    def job_role_researcher(self) -> Agent:
        return create_agent_from_yaml("job_role_researcher", [Tools["perplexity_search_tool"]])
    @task
    def job_role_researcher_task(self) -> Task:
        return create_task_from_yaml("job_role_research_task", agent=self.job_role_researcher())
    
    @agent
    def interview_preparation_researcher(self) -> Agent:
        return create_agent_from_yaml("interview_preparation_researcher",tools=None)
    @task
    def interview_prep_task(self) -> Task:
        return create_task_from_yaml("interview_prep_task", agent=self.interview_preparation_researcher())
    
    @agent
    def reporting_analyst(self) -> Agent:
        return create_agent_from_yaml("reporting_analyst", tools=None, max_iter=3)
    @task
    def reporting_task(self) -> Task:
        return create_task_from_yaml("reporting_task",
                                     agent=self.reporting_analyst(),
                                     output_json=JobInformation,
                                     context=[
                                        self.compensation_career_culture_researcher_task(), 
                                        self.job_role_researcher_task(),
                                        self.interview_prep_task()]
                                    )
    
    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        # print(self.agents)
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            verbose=True,
            planning=True,
            planning_llm="azure/gpt-4o"
        )