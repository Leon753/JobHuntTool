from fastapi import APIRouter, HTTPException
from services.perplexity_client import PerplexityClient 
import os

router = APIRouter()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = os.getenv("PERPLEXITY_API_URL")

perplexity_client = PerplexityClient(
    api_key=PERPLEXITY_API_KEY,
    api_url=PERPLEXITY_API_URL,
    model="your-model"
)

@router.get("/company-job-info")
async def get_company_job_info(company: str, job_position: str):
    # Build the query for the Perplexity API
    query = f"Provide summary about {company} and the job position {job_position} by searching, LinkedIn, \
                Company Career Site, and Indeed for job information. Then searching through LevelsFYI for information \
                about Salary range if the information exists. Also I want to include good problems to do from \
                LeetCode if they exist. Could you also look at GlassDoor and similar sites for information about \
                the interiew process"
    
    response = await perplexity_client.get_response(session=None, prompt=query, response_format={})
    if response is None:
        raise HTTPException(status_code=500, detail="Error fetching data from Perplexity API")
    
    return {"data": response}
