from fastapi import APIRouter, HTTPException
from openai import OpenAI
from services.perplexity_client import PerplexityClient 
from services.openai_client import GPTChatCompletionClient, InMemoryResponseManager
from services.crew_client import LatestAiDevelopmentCrew
from config.keys import PERPLEXITY_API_KEY, OPENAI_GPT4_KEY, ENDPOINT_OPENAI_GPT4, CHAT_VERSION, CHAT_DEPLOYMENT_NAME
import json
import re 
from models.create_table import JobInformation

router = APIRouter()

def string_to_json(response):
    cleaned = re.sub(r"^```json\s*", "", response)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned


@router.get("/email-summary")
async def get_summary_email(email: str):
    messages = [
            {
                "role": "system", 
                "content": "You are an assistant. summarizing an email and prepare a prompt for prepxilty to scrape the web for more information", 
            },
            {
                "role": "user", 
                "content": f"The email content is provided here: {email}"
            }
        ]
    response_manager = InMemoryResponseManager()
    for i in messages:
        response_manager.add_response(role=i["role"], content = i["content"])
    chat_client = GPTChatCompletionClient(response_manager=response_manager, 
                                          base_url=ENDPOINT_OPENAI_GPT4, 
                                          api=OPENAI_GPT4_KEY,
                                          api_version=CHAT_VERSION,
                                          deployment_name=CHAT_DEPLOYMENT_NAME)
    chat_response = chat_client.call(messages=messages)
    msgs = chat_client.parse_response(chat_response)
    for i in msgs:
        chat_client.add_memory(role = "assistant", content = i)
    return {"data": chat_client.get_history()[-1]}



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
                    "content": "<Concise summary of the job posting>",
                    "source": ["<url1>", "<url2>", ...]
                    }},
                    "pay_range": {{
                    "status": "<Validated|Needs Work|Incorrect>",
                    "content": "<Details on the salary range>",
                    "source": ["<url1>", "<url2>", ...]
                    }},
                    "interview_process": {{
                    "status": "<Validated|Needs Work|Incorrect>",
                    "content": "<Details on the interview process, including round counts (behavioral and technical) and overall duration>",
                    "source": ["<url1>", "<url2>", ...]
                    }},
                    "example_interview_experience": {{
                    "status": "<Validated|Needs Work|Incorrect>",
                    "content": "<Example of an interview experience>",
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
        response_format = JobInformation(**response)
    except Exception as e:
        print("ERROR RESPONSE", e)
        raise HTTPException(status_code=500, detail="Response validation failed")

    return {"data": response_format}


@router.get("/company-job-info-crew-ai")
async def get_company_job_info(company: str, job_position: str):
    inputs = {
        'company': company,
        'job': job_position
    }
    result = LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)   
    try:
        response_format = JobInformation(**result.json_dict)
    except Exception as e:
        print("ERROR RESPONSE", e)
        raise HTTPException(status_code=500, detail="Response validation failed")

    return {"data": response_format}