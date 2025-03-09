from fastapi import APIRouter, HTTPException, Query
from services.clients.perplexity_client import PerplexityClient 
from services.clients.crew_client import TableMakerCrew
from config.keys import PERPLEXITY_API_KEY
import json
from models.create_table import JobInformation
from models.email_summary import GPT_Email_Summary_Response
from utils.helpers import string_to_json
from services.summary.email_summary import email_summary
from services.memory import memo_service
from services.spreadsheet_service import create_and_update_spreadsheet

import asyncio
# set up logger 
router = APIRouter()






@router.get("/email-summary")
async def get_summary_email(email: str):
    return email_summary(email)




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
        print("ERROR RESPONSE", e)
        raise HTTPException(status_code=500, detail="Response validation failed")

    try:
        response = JobInformation(**response)
    except Exception as e:
        print("ERROR RESPONSE", e)
        raise HTTPException(status_code=500, detail="Response validation failed")

    return response



@router.post("/company-job-info-crew-ai")
async def get_company_job_info(email:str, token: str = Query(...)):
    summary_json:GPT_Email_Summary_Response = email_summary(email)
    
    query_key = summary_json.company+summary_json.job_position
    inputs = {
        'company': summary_json.company,
        'job': summary_json.job_position,
        'summary': summary_json.summary,
        "status": str(summary_json.status)
    }

    if await memo_service.query_exists(query_key):
        response_dict = await memo_service.get_response_for_query(query_key)
        try:
            response_format = JobInformation(**response_dict)
        except Exception as e:
            print("ERROR RESPONSE", e)
            raise HTTPException(status_code=500, detail="Response validation failed")
    else:
        result = await asyncio.to_thread(TableMakerCrew().crew().kickoff, inputs) 
        await memo_service.save_query_response(query_key, result.json_dict)
        try:
            response_format = JobInformation(**result.json_dict)
        except Exception as e:
            print("ERROR RESPONSE", e)
            raise HTTPException(status_code=500, detail="Response validation failed")

    
    try:
        spreadsheet_result = await create_and_update_spreadsheet(token, response_format)
    except Exception as e:
        print("Spreadsheet update error:", e)
        raise HTTPException(status_code=500, detail="Failed to update spreadsheet")

    return {"spreadsheet": spreadsheet_result}