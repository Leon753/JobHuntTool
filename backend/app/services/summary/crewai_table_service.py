from services.clients.crew_client import TableMakerCrew
from services.memory import memo_service
import asyncio
from models.create_table import JobInformation
from config.logger import logger

async def crewai_table(query_key:str, inputs:dict):
    try:
        print("here1")
        crew  = TableMakerCrew()
        print("here2")
        crew = crew.crew()
        print("here3")
        result = await asyncio.to_thread(crew.kickoff, inputs) 
        await memo_service.save_query_response(query_key, result.json_dict)
        response_format = JobInformation(**result.json_dict)
        return response_format
    except BaseException as e:
        logger.error(f"ERROR RESPONSE: from crew ai kickoff {e}")
        raise Exception from e
    
       
    
