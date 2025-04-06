from services.user.user_service import save_user_info_to_db
from services.clients.google_client.sheets_client import create_sheet, update_sheet, update_sheet_format
from typing import Dict, Tuple
from config.logger import logger
from config.sheets_format import *
from models.email_summary import Status
from services.format.sheet_formater import SheetFormatter

async def create_new_sheet_for_user(
        authorization: str, 
        user_id: str, 
        title: str = None
    ) -> Tuple[str, int]:
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
    await apply_new_sheet_formatting(authorization, excel_id)
    await auto_resize_wrap_columns(authorization, excel_id)

    # 3) Record spreadsheet ID in your DB
    start_row = 2  # We'll start adding data from row 2
    await save_user_info_to_db(user_id, start_row, excel_id)

    return excel_id, start_row


async def update_google_sheets_row(
        authorization: str, 
        user_id: str, 
        excel_id:str, 
        row:int, 
        row_values: list
    ) -> None:
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


async def apply_new_sheet_formatting(
        authorization: str,
        spreadsheet_id: str, 
        sheet_id:int = 0
    ) -> None:

    formatter = SheetFormatter(sheet_id)
    batch_update_json = (
        formatter
        .clear_format() # Clear existing formatting to start fresh
        .set_header_format(
            0, 
            TABLE_SIZE_COLUMN, 
            {"red": 0.7176, "green": 0.8824, "blue": 0.8039, "alpha": 1.0}
        )  # Set header format
        .auto_resize(
            0, 
            TABLE_SIZE_COLUMN
        )
        .add_conditional_format_rule(
            condition_value=str(Status.OFFER.value),  # e.g. "interviewing"
            background_color={"red": 0.0, "green": 0.7, "blue": 0.0, "alpha": 1.0}, # Light gray for offer
            start_row=1,
            end_row=TABLE_SIZE_ROW,
            start_col=HEADER_NAMES.index("STATUS"),  # Assuming "Status" is the column for status
            end_col=HEADER_NAMES.index("STATUS") + 1,  # End column is exclusive, so +1
            index=0
        )
        .add_conditional_format_rule(
            condition_value=str(Status.REJECTED.value),  # e.g. "interviewing"
            background_color={"red": 1.0, "green": 0.0, "blue": 0.0, "alpha": 1.0},
            start_row=1,
            end_row=TABLE_SIZE_ROW,
            start_col=HEADER_NAMES.index("STATUS"),     # Assuming "Status" is the column for status
            end_col=HEADER_NAMES.index("STATUS") + 1,   # End column is exclusive, so +1
            index=0
        ) # Clear any existing banded rows to avoid conflicts
        .add_banded_rows(
            start_row=1,  # Start from the first row after the header
            end_row=TABLE_SIZE_ROW,  # End at the last row of the table
            start_col=0,  # Start from the first column
            end_col=TABLE_SIZE_COLUMN,  # End at the last column
            first_band_color={"red": 0.95, "green": 0.95, "blue": 0.95, "alpha":1.0},  # Light gray for banded rows
            second_band_color={"red": 1.0, "green": 1.0, "blue": 1.0, "alpha":1.0},  # White for alternating rows
        )
        .build()  
    )
    await update_sheet_format(authorization,
                              batch_update_json,
                              spreadsheet_id)

async def auto_resize_wrap_columns(
        authorization: str, 
        spreadsheet_id: str, 
        sheet_id:int = 0
    ) -> None:
    """
    Auto-resizes the columns of the Google Sheet to fit their content.
    
    Args:
        authorization (str): Bearer token for Google Sheets.
        spreadsheet_id (str): The ID of the spreadsheet to update.
        sheet_id (int): The ID of the sheet to apply formatting to. Defaults to 0.
        
    Returns:
        None
    """

    formatter = SheetFormatter(sheet_id)
    batch_update_json = (
        formatter
        .set_column_width(
            0, 
            HEADER_NAMES.index("STATUS")+1,  # Set width for all columns up to JOB_DESCRIPTION
            pixel_size=85
        )
        .set_column_width(
            HEADER_NAMES.index("JOB_DESCRIPTION"),  # Set width for the JOB_DESCRIPTION column
            TABLE_SIZE_COLUMN,  # Set width for all columns after JOB_DESCRIPTION
            pixel_size=500 # Wider width for job description to accommodate more text
        )
        .wrap_and_allign_text(
            start_row=1, 
            end_row=TABLE_SIZE_ROW,
            start_col=0, 
            end_col=HEADER_NAMES.index("STATUS")+1,  
            vertical_alignment="MIDDLE",  
            horizontal_alignment="CENTER", 
            font_size=12
        )
        .wrap_and_allign_text(
            start_row=1,  # Start from the first row after the header
            end_row=TABLE_SIZE_ROW,  # End at the last row of the table
            start_col=HEADER_NAMES.index("JOB_DESCRIPTION"),  # Start from the first column
            end_col=TABLE_SIZE_COLUMN,
            vertical_alignment="TOP", 
            font_size=12
        )  # Resize all columns in the sheet
        .build()
    )
    await update_sheet_format(authorization, batch_update_json, spreadsheet_id)

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