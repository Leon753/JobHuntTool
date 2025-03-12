from fastapi import APIRouter, HTTPException, Request, Header
from services.clients.perplexity_client import PerplexityClient 
from services.clients.crew_client import TableMakerCrew
from config.keys import PERPLEXITY_API_KEY
import json
from models.create_table import *
from models.email_summary import GPT_Email_Summary_Response, Status
from utils.helpers import string_to_json
from services.summary import email_summary_service
from services.memory import memo_service
from services.summary  import crewai_table_service
from services.user  import user_service
from services.google import email, sheets
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
        print("ERROR RESPONSE", e)
        raise HTTPException(status_code=500, detail="Response validation failed")

    try:
        response = JobInformation(**response)
    except Exception as e:
        print("ERROR RESPONSE", e)
        raise HTTPException(status_code=500, detail="Response validation failed")

    return response






def get_columns_content_strings(columns: Columns) -> dict[str, str]:
    """
    Given a Columns instance, return a dictionary mapping each column field name to a single string.
    The string is constructed by joining the content list items with a newline character.
    """
    result = {}
    # Convert the pydantic model to a dict for readability.
    columns_data = columns.model_dump()
    for column_name, data in columns_data.items():
        # 'data' is a dict with keys: status, content, source.
        # We join the items in the 'content' list.
        content_list = data.get("content", [])
        result[column_name] = "\n".join(content_list)
    return result

@router.post("/company-job-info-crew-ai/")
async def get_company_job_info( payload:TableRowRequestPayload, authorization: str = Header(...) ):
    summary_json:GPT_Email_Summary_Response = await email_summary_service.email_summary(payload.email_content)

    match(summary_json.status): 
        case Status.IN_REVIEW | Status.INTERVIEWING:
            query_key = summary_json.company+summary_json.job_position
            if await memo_service.query_exists(query_key):
                response_dict = await memo_service.get_response_for_query(query_key)
                try:
                    response_format = JobInformation(**response_dict)
                except Exception as e:
                    print("ERROR RESPONSE", e)
                    raise HTTPException(status_code=500, detail="Response validation failed")
            else: 
                inputs = {
                    'company': summary_json.company,
                    'job': summary_json.job_position,
                    'summary': summary_json.summary,
                    "status": str(summary_json.status)
                }
                try:
                    response_format:JobInformation = await crewai_table_service.crewai_table(query_key=query_key, inputs=inputs)
                except Exception as e:
                    raise HTTPException(status_code=500, detail="Response validation failed")

           
            user_service_response = await user_service.get_user_excel_from_db(user_id=payload.user_id)
            if user_service_response is None:
                row = 2
                data = {
                    "properties": { "title": "BACKEND JobHuntingTest" }
                }   
                res = await sheets.createSheet(authorization, data)
                excel_id = res['spreadsheetId']
                await user_service.save_user_info_to_db(user_id=payload.user_id,
                                                        current_sheet_row=1, 
                                                        excel_id=res['spreadsheetId'])
            else :
               
                row  = user_service_response["current_sheet_row"]
                excel_id = user_service_response["excel_id"]

            sheets_data = {
                "valueInputOption": "USER_ENTERED",
                "data": [],
                "includeValuesInResponse": "false",
                "responseValueRenderOption": "FORMATTED_VALUE",
                "responseDateTimeRenderOption": "SERIAL_NUMBER"
            }
            if row == 2:
                headerDataItem = {
                        "range": f"{HEADER_COLUMNS[0]}1:{HEADER_COLUMNS[-1]}1",
                        "majorDimension": "ROWS",
                        "values": [HEADER_NAMES]
                    }
                sheets_data["data"].append(headerDataItem)


            content_strings = get_columns_content_strings(response_format.results)
            row_values = [
                summary_json.company,           
                summary_json.job_position,      
                str(summary_json.status.name),  
                content_strings["job_description"],
                content_strings["pay_range"],
                content_strings["interview_process"],
                content_strings["example_interview_experience"]
            ]

            
            rowDataItem = {
                "range": f"{HEADER_COLUMNS[0]}{row}:{HEADER_COLUMNS[-1]}{row}",
                "majorDimension": "ROWS",
                "values": [row_values]
            }
            sheets_data["data"].append(rowDataItem)
            
            res = await sheets.updateSheet(authorization, sheets_data, excel_id)
            await user_service.update_user_row(user_id=payload.user_id, current_sheet_row=row+1)

            
        case Status.OFFER | Status.REJECTED:
            return " UPDATE DATABASE"
        case _:
            raise HTTPException(status_code=500, detail="Response validation failed")

        
        

        

    