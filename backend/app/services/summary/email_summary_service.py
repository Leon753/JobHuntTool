from services.clients.openai_client import *
from config.keys import *
from models.email_summary import *
import json
from schemas.email_schema import email_schema
from utils.helpers import string_to_json

async def email_summary(email:str) -> GPT_Email_Summary_Response:

    query  = f"""
            Provide a summary of the email and also extract the job and company from the email. 
             
             The email content is provided here: {email}. 
             
            
             
             Return a JSON schema with the following keys: 

             {{
             
                "company": **insert company name here**,
                "job_position": **insert job position here**,
                "summary": **insert summary here**
                "status": **insert Enum One of: InReview, Interviewing, Offer, Rejected**
            }}
            """
    messages = [
        {
            "role": "system", 
            "content": "You are an assistant. summarizing an email and prepare a prompt for prepxilty to scrape the web for more information", 
        },
        {
            "role": "user", 
            "content":query
        }
        
    ]
   
    chat_client = GPTChatCompletionClient(base_url=ENDPOINT_OPENAI_GPT4, 
                                          api=OPENAI_GPT4_KEY,
                                          api_version=CHAT_VERSION,
                                          deployment_name=CHAT_DEPLOYMENT_NAME)
    response_format = {
            "type": "json_schema",
        "json_schema": {"name": "email_schema", "schema": GPT_Email_Summary_Response.model_json_schema()}
    }
    
    chat_response = await chat_client.call_async(messages=messages, response_format=response_format)
    msgs = chat_client.parse_response(chat_response)
    try: 
        # msg  =  string_to_json(msgs[-1])
        response = json.loads(msgs[-1])
    except Exception as e:
        print("ERROR RESPONSE", e)
        raise SyntaxError("Response validation failed")
    
    try :
        response_format = GPT_Email_Summary_Response(**response)
    except Exception as e:
        print("ERROR RESPONSE", e)
        raise SyntaxError("Response validation failed")
    
    return response_format


