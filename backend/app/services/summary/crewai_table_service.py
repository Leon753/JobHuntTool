
from services.memory import memo_service
import asyncio
from models.create_table import JobInformation
from config.logger import logger
from crewai.crews import CrewOutput
import asyncio
from services.clients.crew_client.agents.table_agent import TableMakerCrew

async def crewai_table(query_key:str, inputs:dict):
    try:
        table_maker_instance = TableMakerCrew()
        result = await table_maker_instance.crew().kickoff_async(inputs=inputs)
        await memo_service.save_query_response(query_key, result.json_dict)
        response_format = JobInformation(**result.json_dict)
        return response_format
    except BaseException as e:
        logger.error(f"ERROR RESPONSE: from crew ai kickoff {e}")
        raise Exception from e
    
       
    
