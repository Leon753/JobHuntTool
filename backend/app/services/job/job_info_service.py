
from services.memory import memo_service
from services.summary import crewai_table_service
from models.create_table import JobInformation
from models.email_summary import GPT_Email_Summary_Response
from config.logger import logger
from fastapi import HTTPException

async def get_or_create_job_info(
    query_key: str, 
    summary_json:GPT_Email_Summary_Response
) -> JobInformation:
    """
    Returns a JobInformation object, either from memoized storage
    or by calling the CrewAI table service.
    """
    if await memo_service.query_exists(query_key):
        # If memoized, retrieve from DB
        response_dict = await memo_service.get_response_for_query(query_key)
        try:
            return JobInformation(**response_dict)
        except Exception as e:
            logger.error(f"ERROR RESPONSE: {e}")
            raise HTTPException(status_code=500, detail="Response validation failed")
    else:
        # Otherwise, call CrewAI and store in memo
        inputs = {
            'company': summary_json.company,
            'job': summary_json.job_position,
            'summary': summary_json.summary,
            "status": str(summary_json.status)
        }
        try:
            return await crewai_table_service.crewai_table(query_key=query_key, inputs=inputs)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Response validation failed")