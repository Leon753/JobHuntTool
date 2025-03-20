from services.clients.google_client import email_client
from utils.helpers import decode_email_parts
from services.summary import email_summary_service

async def get_email(authorization: str, email_id: str):
    email_response = await email_client.get_email_client(authorization, email_id)
    return email_response

async def get_email_summary(email_response):
    results = decode_email_parts(email_response['payload']['parts'])[0]
    user_id = email_response['payload']['headers'][0]['value']
    return await email_summary_service.email_summary(results)
