# spreadsheet_service.py
import httpx
from fastapi import HTTPException
from typing import List
from models.create_table import JobInformation  # Ensure this import is correct

def get_column_letter(col_index: int) -> str:
    """Convert a 1-based column index to its corresponding Excel column letter."""
    letter = ""
    while col_index > 0:
        remainder = (col_index - 1) % 26
        letter = chr(65 + remainder) + letter
        col_index = (col_index - 1) // 26
    return letter

def get_first_index_values(job_info: JobInformation) -> List[str]:
    """
    Given a JobInformation instance, returns a list containing
    the first element of each JobDetail's content.
    Adjust the fields as needed.
    """
    values = []
    # Example: assuming job_info has these attributes with a 'content' list.
    for field in [
        job_info.job_description,
        job_info.pay_range,
        job_info.interview_process,
        job_info.example_interview_experience
    ]:
        if field.content and len(field.content) > 0:
            values.append(field.content[0])
        else:
            values.append("")
    return values

async def create_and_update_spreadsheet(token: str, response_format: JobInformation) -> dict:
    """
    Creates a new spreadsheet and updates it with the provided job information.
    Expects a token with the necessary Sheets API scopes.
    """
    values = get_first_index_values(response_format)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    spreadsheet_request_body = {"properties": {"title": "JobHunting"}}
    
    async with httpx.AsyncClient() as client:
        create_response = await client.post(
            "https://sheets.googleapis.com/v4/spreadsheets",
            headers=headers,
            json=spreadsheet_request_body
        )
    
    if create_response.status_code != 200:
        raise HTTPException(status_code=create_response.status_code, detail="Failed to create spreadsheet")
    
    spreadsheet_data = create_response.json()
    spreadsheet_id = spreadsheet_data.get("spreadsheetId")
    if not spreadsheet_id:
        raise HTTPException(status_code=500, detail="Spreadsheet ID not returned")
    
    num_cols = len(values)
    end_col = get_column_letter(num_cols)
    range_str = f"A1:{end_col}1"
    
    update_body = {
        "valueInputOption": "USER_ENTERED",
        "data": [{
            "range": range_str,
            "majorDimension": "ROWS",
            "values": [values]
        }]
    }
    
    async with httpx.AsyncClient() as client:
        update_response = await client.post(
            f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values:batchUpdate",
            headers=headers,
            json=update_body
        )
    
    if update_response.status_code != 200:
        raise HTTPException(status_code=update_response.status_code, detail="Failed to update spreadsheet")
    
    return {
        "spreadsheetId": spreadsheet_id,
        "updateResponse": update_response.json()
    }