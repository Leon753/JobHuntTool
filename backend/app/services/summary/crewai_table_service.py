from services.clients.crew_client import TableMakerCrew
from services.memory import memo_service
import asyncio
from models.create_table import JobInformation
from config.logger import logger

async def crewai_table(query_key:str, inputs:dict):
    try:
        result = await asyncio.to_thread(TableMakerCrew().crew().kickoff, inputs) 
        await memo_service.save_query_response(query_key, result.json_dict)
        response_format = JobInformation(**result.json_dict)
        return response_format
    except Exception as e:
        logger.error(f"ERROR RESPONSE: {e}")
        raise Exception from e
    
