from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.get("/company-job-info")
def get_company_job_info(company: str, job_position: str):
    # Build the query for the Perplexity API
    query = f"Provide summary about {company} and the job position {job_position} by searching, LinkedIn, \
                Company Career Site, and Indeed for job information. Then searching through LevelsFYI for information \
                about Salary range if the information exists. Also I want to include good problems to do from \
                LeetCode if they exist. Could you also look at GlassDoor and similar sites for information about \
                the interiew process"
    
    api_url = "https://api.perplexity.ai/search"
    
    headers = {
        "Authorization": "Bearer YOUR_API_KEY"
    }
    
    params = {
        "query": query
    }
    
    response = requests.get(api_url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Perplexity API")
    
    return response.json()
