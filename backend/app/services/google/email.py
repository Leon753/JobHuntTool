from services.clients.async_client import client
from config.logger import logger
async def getEmail(headers: str, emailId: str):
    try:
        headerValues = {
            "Authorization": headers,
            "Content-Type": "application/json",
        }
        response = await client.get(f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{emailId}?format=full', headers=headerValues)
        if response.status_code == 200:
            return response.json()
    except Exception as error:
        logger.error(f"An error occurred: {error}")
        return error
