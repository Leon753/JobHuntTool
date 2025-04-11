import base64
import re
from models.create_table import Columns , JobInformation
from models.email_summary import GPT_Email_Summary_Response
from config.logger import logger
from datetime import datetime
def string_to_json(response):
    cleaned = re.sub(r"^```json\s*", "", response)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned

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
        # TODO: THIS IS A BUG
        if len(content_list) == 0:
            logger.warning("THERE IS AN EMPTY OUTPUT FROM REPORTING AGENT: MEANING THE SECTION WILL BE EMPTY")
            result[column_name] = " " 
            continue
        if column_name == "pay_range":
            # For pay_range, we need to format it differently.
            formatted = [f"*{item['position']}: {item['salary']}" for item in content_list]
            result[column_name] = "\n".join(formatted) 
            continue
        content_list[0] = "*" + content_list[0]
        result[column_name] = "\n*".join(content_list)
    return result

def extract_row_values(response:JobInformation, summary_json:GPT_Email_Summary_Response) -> list:
    content_strings = get_columns_content_strings(response.results) 
    # Get today's date and format it as 'YYYY-MM-DD'
    row_values = [
        summary_json.company,           
        summary_json.job_position, 
        datetime.today().strftime('%Y-%m-%d'),
        str(summary_json.status.value),  
        response.industry,
        response.location,
        response.score,
        content_strings["years_of_experience"],
        content_strings["job_description"],
        content_strings["pay_range"],
        content_strings["interview_process"],
        content_strings["example_interview_experience"],
        content_strings["career_growth"],
        content_strings["example_technical_questions"],
        
    ]
    return row_values

def decode_email_parts(email_parts: list) -> list:
    decoded_results = []
    for part in email_parts:
        # Extract the data from the part dictionary.
        data = part.get('body', {}).get('data', '')
        if data:
            # Convert URL-safe Base64 to standard Base64.
            b64 = data.replace('-', '+').replace('_', '/')
            # Add missing padding if needed.
            padding = len(b64) % 4
            if padding:
                b64 += '=' * (4 - padding)
            # Decode the Base64 string into bytes, then decode to a UTF-8 string.
            decoded_string = base64.b64decode(b64).decode('utf-8')
            decoded_results.append(decoded_string)
    return decoded_results
