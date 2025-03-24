
from services.memory import memo_service
import asyncio
from models.create_table import JobInformation
from config.logger import logger
from crewai.crews import CrewOutput
from services.clients.crew_client.agents import company_researcher_agent, financial_researcher_agent, compensation_researcher_agent, reporter_agent
from services.clients.crew_client.agents import interview_researcher_agent, job_role_researcher_agent, reference_researcher_agent, mission_researcher_agent
class Crew_Wrapper(): 
    def __init__(self):
        # Create instances for each Crew
        self.company_researcher_instance = company_researcher_agent.CompanyResearcher()
        self.mission_researcher_instance = mission_researcher_agent.MissionResearcher()
        self.financial_researcher_instance = financial_researcher_agent.FinancialResearcher()
        self.job_role_researcher_instance = job_role_researcher_agent.JobRoleResearcher()
        self.interview_reseacher = interview_researcher_agent.InterviewReseacher()
        self.reporter_instance = reporter_agent.Reporter()
    
    async def run_tasks(self, inputs: dict) -> CrewOutput:
        """
        Kick off all research crews concurrently using the same input dictionary.
        """
        tasks = [
                self.company_researcher_instance.crew().kickoff_async(inputs=inputs),
                self.mission_researcher_instance.crew().kickoff_async(inputs=inputs),
                self.job_role_researcher_instance.crew().kickoff_async(inputs=inputs),
                self.interview_reseacher.crew().kickoff_async(inputs=inputs),
        ]
        logger.info("Starting all crews concurrently.")
        all_results = await asyncio.gather(*tasks)
        inputs["research"] = [ i.raw for i in all_results]
        report = await self.get_report(inputs)
        return report

    async def get_report(self, inputs):
        report = await self.reporter_instance.crew().kickoff_async(inputs=inputs)
        return report



        

async def crewai_table(query_key:str, inputs:dict):
    try:
        cw = Crew_Wrapper()
        result = await cw.run_tasks(inputs)
        await memo_service.save_query_response(query_key, result.json_dict)
        response_format = JobInformation(**result.json_dict)
        return response_format
    except BaseException as e:
        logger.error(f"ERROR RESPONSE: from crew ai kickoff {e}")
        raise Exception from e
    
       
    
