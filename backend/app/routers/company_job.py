from fastapi import APIRouter, HTTPException
from services.perplexity_client import PerplexityClient 
from services.openai_client import GPTChatCompletionClient, GPTCompletionClient, InMemoryResponseManager
from dotenv import load_dotenv
from pydantic import BaseModel
import os

router = APIRouter()
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = os.getenv("PERPLEXITY_API_URL")
OPENAI_GPT4_KEY = os.getenv("AZURE_OPENAI_KEY_GPT_4")
ENDPOINT_OPENAI_GPT4 = os.getenv("GPT4_ENDPOINT")

CHAT_VERSION = "2024-08-01-preview"  # Update if needed
CHAT_DEPLOYMENT_NAME = "gpt-4o"  # Replace with your deployed model name

perplexity_client = PerplexityClient(
    api_key=PERPLEXITY_API_KEY,
    api_url=PERPLEXITY_API_URL,
    model="your-model"
)


class Email_Summary_Request(BaseModel):
    content: str

@router.post("/email-summary")
async def get_summary_email(packet: Email_Summary_Request):
    messages = [
            {
                "role": "system", 
                "content": "You are an assistant. summarizing an email and prepare a prompt for prepxilty to scrape the web for more information", 
            },
            {
                "role": "user", 
                "content": f"The email content is provided here: {packet.content}"
            }
        ]
    response_manager = InMemoryResponseManager()
    for i in messages:
        response_manager.add_response(role=i["role"], content = i["content"])
    chat_client = GPTChatCompletionClient(response_manager=response_manager, 
                                          base_url=ENDPOINT_OPENAI_GPT4, 
                                          api=OPENAI_GPT4_KEY,
                                          deployment_name=CHAT_DEPLOYMENT_NAME)
    chat_response = chat_client.call(messages=messages)
    msgs = chat_client.parse_response(chat_response)
    for i in msgs:
        chat_client.add_memory(role = "assistant", content = i)
    return {"data": chat_client.get_history()[-1]}


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
