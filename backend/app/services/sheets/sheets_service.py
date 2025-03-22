from services.user.user_service import get_user_excel_from_db, save_user_info_to_db, update_user_row
from services.clients.google_client.sheets_client import create_sheet, update_sheet, update_sheet_format
from typing import Dict, Tuple
from config.logger import logger
from config.sheets_format import sheet_format_json

HEADER_COLUMNS = ["A","B","C","D","E","F","G","H","I"]
HEADER_NAMES = [
    "COMPANY",
    "POSITION",
    "STATUS",
    "JOB_DESCRIPTION",
    "PAY_RANGE",
    "INTERVIEW_PROCESS",
    "EXAMPLE_INTERVIEW_EXPERIENCE",
    "CAREER_GROWTH",
    "EXAMPLE_TECHNICAL_QUESTIONS"
]

async def create_new_sheet_for_user(authorization: str, user_id: str, title: str = None) -> Tuple[str, int]:
    """
    Creates a new Google Sheet for the user if none exists and returns (spreadsheet_id, start_row).
    
    Args:
        authorization (str): Bearer token/OAuth2 token for Google Sheets.
        user_id (str): The ID representing the user in your system.
        title (str, optional): Title for the new sheet. Defaults to None.
        
    Returns:
        Tuple[str, int]: The new spreadsheet ID and the starting row (e.g., 2).
    """
    if not title:
        title = f"BACKEND JobHuntingForUser_{user_id}"
    # This is the payload required by Google's createSheet API
    data = {"properties": {"title": title}}
    
    # 1) Create a new sheet via the Sheets client
    response = await create_sheet(authorization, data)
    excel_id = response["spreadsheetId"]

     # 2) insert header rows here by calling `update_sheet` 
    header_data = {
        "valueInputOption": "USER_ENTERED",
        "data": [{
            "range": f"{HEADER_COLUMNS[0]}1:{HEADER_COLUMNS[-1]}1",
            "majorDimension": "ROWS",
            "values": [HEADER_NAMES]
        }]
    }
    await update_sheet(authorization, header_data, excel_id)

    # 3) Record spreadsheet ID in your DB
    start_row = 2  # We'll start adding data from row 2

    return excel_id, start_row


async def update_google_sheets_row(authorization: str, user_id: str, excel_id:str, row:int, row_values: list) -> None:
    """
    Updates the user's Google Sheet with the provided row data.
    
    If the user doesn't have a sheet yet, create it first.
    Then append a new row using the row_values list.
    
    Args:
        authorization (str): Bearer token for Google Sheets.
        user_id (str): The ID representing the user.
        row_values (list): The data to write in a single row (e.g. 
            [company, position, status, job_description, ...]).
    
    Returns:
        None
    """
    # 2) Prepare the Sheets batchUpdate payload
    sheets_data = {
        "valueInputOption": "USER_ENTERED",
        "data": [{
            "range": f"{HEADER_COLUMNS[0]}{row}:{HEADER_COLUMNS[-1]}{row}",
            "majorDimension": "ROWS",
            "values": [row_values]  
        }]
    }
    # 3) Send update to Google Sheets
    await update_sheet(authorization, sheets_data, excel_id)


async def apply_sheet_formatting(authorization: str,spreadsheet_id: str, sheet_id:int = 0):
    await update_sheet_format(authorization,sheet_format_json,spreadsheet_id)


async def update_status_column(authorization: str, user_id: str, excel_id:str, row:int, row_value: list):
    sheets_data = {
        "valueInputOption": "USER_ENTERED",
        "data": [{
            "range": f"{HEADER_COLUMNS[HEADER_NAMES.index("STATUS")]}{row}",
                "majorDimension": "ROWS",
                "values": [row_value]
        }]
    }
    res = await update_sheet(authorization, sheets_data, excel_id)