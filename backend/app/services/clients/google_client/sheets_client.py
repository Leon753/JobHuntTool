from services.clients.async_client import client
from config.logger import logger
from utils.exception.google_exception import GoogleSheetsAPIError
import json

async def create_sheet(auth_header: str, body: dict) -> dict:
    if not auth_header:
        raise ValueError("Missing authorization header")
    headerValues = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
        }

    logger.debug("Sending payload to Google Sheets API:\n" + json.dumps(body, indent=2))
    response = await client.post("https://sheets.googleapis.com/v4/spreadsheets", headers=headerValues, json=body)

    try:
        response.raise_for_status()
        logger.info("Google Sheets Create API request successful.")
        return response.json()
  
    except Exception as e:
        logger.error(f"Google Sheets API Error:  {e.response.status_code}: details : {e.response.text}")
        raise GoogleSheetsAPIError(e.response) from e

async def update_sheet(auth_header: str, body: dict, spreadsheetId: str) -> dict:
    if not auth_header:
            raise ValueError("Missing authorization header")
        
    headerValues = {
        "Authorization": auth_header,
        "Content-Type": "application/json",
    }
    
    logger.debug("Sending payload to Google Sheets API:\n" + json.dumps(body, indent=2))
    response = await client.post(f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values:batchUpdate", headers=headerValues, json=body)
    try:
        response.raise_for_status()
        logger.info("Google Sheets API request successful.")
        return response.json()
  
    except Exception as e:
        logger.error(f"Google Sheets API Error {e.response.status_code}: details : {e.response.text}")
        raise GoogleSheetsAPIError(e.response) from e

async def update_sheet_format(auth_header: str, body: dict, spreadsheetId: str) -> dict:
    if not auth_header:
        raise ValueError("Missing authorization header")
        
    headerValues = {
        "Authorization": auth_header,
        "Content-Type": "application/json",
    }
    logger.debug("Sending payload to Google Sheets API:\n" + json.dumps(body, indent=2))    
    response = await client.post(f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}:batchUpdate", headers=headerValues, json=body)

    try:
        response.raise_for_status()
        logger.info("Google Sheets Update API request successful.")
        return response.json()
  
    except Exception as e:
        logger.error(f" Google Sheets API Error{e.response.status_code}: details : {e.response.text}")
        raise GoogleSheetsAPIError(e.response) from e