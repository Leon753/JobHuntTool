import json
from models.create_table import JobInformation
from fastapi import APIRouter, HTTPException, Header, Body
from services.clients.perplexity_client import PerplexityClient 
from config.keys import PERPLEXITY_API_KEY
from models.email_summary import GPT_Email_Summary_Response, Status
from utils.helpers import string_to_json
from services.summary import email_summary_service
from services.job import job_status_service
from config.logger import logger
from services.email import email_service

# set up logger 
router = APIRouter() 

@router.get("/email-summary")
async def get_summary_email(email: str):
    return await email_summary_service.email_summary(email)

@router.get("/company-job-info")
async def get_company_job_info(company: str, job_position: str):
    # Build the query for the Perplexity API
    query = f"""
        Task:
            - Provide a comprehensive summary about {company} and the job position {job_position}. Gather the following information:
            1. **Job Description:**
                - Search LinkedIn, the Company Career Site, Indeed, and Glassdoor for the job posting details.
            2. **Salary/Pay Range:**
                - Search http://levels.fyi/ for details on the salary range for {job_position} at {company}.
            3. **Interview Process:**
                - Gather insights from interview process reviews.
                - Identify whether the technical interviews are more focused on algorithms or data structures.
                - Explicity specify the range of total number of rounds, breaking them down into behavioral and technical rounds.
                - Include the typical overall duration of the interview process.
            4. **Interview Experience:**
                - Find an example of an interview experience for {job_position} at {company}.
            5. **Recommended Preparation:**
                - Search Reddit and Leetcode for recommended Leetcode problems for {company}.

            Output Requirements:
            - Output a JSON object in the following format, and do not include any additional text or markdown:

            {{
                "company": "{company}",
                "results": {{
                    "job_description": {{
                    "status": "<Validated|Needs Work|Incorrect>",
                    "content": "List<Concise summary of the job posting>",
                    "source": ["<url1>", "<url2>", ...]
                    }},
                    "pay_range": {{
                    "status": "<Validated|Needs Work|Incorrect>",
                    "content": "List<Details on the salary range>",
                    "source": ["<url1>", "<url2>", ...]
                    }},
                    "interview_process": {{
                    "status": "<Validated|Needs Work|Incorrect>",
                    "content": "List<Details on the interview process, including round counts (behavioral and technical) and overall duration>",
                    "source": ["<url1>", "<url2>", ...]
                    }},
                    "example_interview_experience": {{
                    "status": "<Validated|Needs Work|Incorrect>",
                    "content": "List<Example of an interview experience>",
                    "source": ["<url1>", "<url2>", ...]
                    }}
                }}
            }}
    """
    messages = [
        {
            "role": "system",
            "content": (
                "Give a consice but informative answer"
            ),
        },
        {   
            "role": "user",
            "content": (
                query
            ),
        },
    ]
    response_format = {
		    "type": "json_schema",
        "json_schema": {"schema": JobInformation.model_json_schema()}
    }
    prelixty_client = PerplexityClient(api_key=PERPLEXITY_API_KEY, 
                                       api_url="https://api.perplexity.ai/chat/completions", 
                                       model="sonar")
    response = await prelixty_client.get_response(messages=messages, response_format=response_format)

    try:
        response = json.loads(string_to_json(response))
    except Exception as e:
        logger.error(f"ERROR RESPONSE {e}")
        raise HTTPException(status_code=500, detail="Response validation failed")

    try:
        response = JobInformation(**response)
    except Exception as e:
        logger.error(f"ERROR RESPONSE {e}")
        raise HTTPException(status_code=500, detail="Response validation failed")

    return response



@router.post("/company-job-info-crew-ai")
async def get_company_job_info( email_id: str = Body(...), authorization: str = Header(...) ):
    logger.info("INFO CREW AI CALLED")
    
    # Step 1: Get email content
    email_response = await email_service.get_email(authorization, email_id)
    user_id = email_response['payload']['headers'][0]['value']
    summary_json: GPT_Email_Summary_Response = await email_service.get_email_summary(email_response)
    
    # Step 2: Process job application based on status using match-case
    match(summary_json.status): 
        case Status.IN_REVIEW | Status.INTERVIEWING:
            await job_status_service.handle_in_review_or_interview(summary_json,user_id, authorization)
            return {"message": "Job info successfully updated"}

        case Status.OFFER | Status.REJECTED:
            msg = await job_status_service.handle_offer_or_rejection(summary_json, user_id, authorization)
            return {"message": msg}
        case _:
            raise HTTPException(status_code=500, detail="Response validation failed")
        
