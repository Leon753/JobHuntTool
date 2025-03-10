from services.clients.async_client import client

async def getEmail(headers: dict, emailId: str):
    try:
        auth_header = headers.get("authorization")
        if not auth_header:
            raise ValueError("Missing authorization header")
        
        headerValues = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
        }
        response = await client.get(f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{emailId}?format=full', headers=headerValues)
        if response.status_code == 200:
            return response.json()
    except Exception as error:
        print(f"An error occurred: {error}")
        return error
