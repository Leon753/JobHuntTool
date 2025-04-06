import json
from services.job import job_url_service
from services.tools.web_scraper_tool import WebScrapperTool
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
        
@router.post("/company-job-url-crew-ai")
async def get_company_job_url(user_id: str = Body(...), job_post_url: str = Body(...), authorization: str = Header(...)):
    logger.info("INFO CREW AI CALLED")

    scraped_response = job_url_service.get_job_link_info(job_post_url)
    # Use job posting content as the "email"
    summary_json: GPT_Email_Summary_Response = await email_summary_service.email_summary(scraped_response)

    # Assume the user is in the Interviewing phase
    await job_status_service.handle_in_review_or_interview(summary_json,user_id, authorization)
    return {"message": "Job info successfully updated"}
