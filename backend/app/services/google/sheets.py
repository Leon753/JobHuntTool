from services.clients.async_client import client

async def createSheet(headers: dict, body: dict) -> dict:
    try:
        auth_header = headers.get("authorization")
        if not auth_header:
            raise ValueError("Missing authorization header")
        
        headerValues = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
        }

        response = await client.post("https://sheets.googleapis.com/v4/spreadsheets", headers=headerValues, json=body)
        if response.status_code == 200:
            print(response)
            return response.json()
        
        return {"error": f"Unexpected status {response.status_code}", "details": response.text}
    except Exception as error:
        print(f"An error occurred: {error}")
        return {"error": str(error)}

async def updateSheet(headers: dict, body: dict, spreadsheetId: str) -> dict:
    try:
        auth_header = headers.get("authorization")
        if not auth_header:
            raise ValueError("Missing authorization header")
        
        headerValues = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
        }
        response = await client.post(f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values:batchUpdate", headers=headerValues, json=body)
        if response.status_code == 200:
            print(response)
            return response.json()
        
        return {"error": f"Unexpected status {response.status_code}", "details": response.text}
    except Exception as error:
        print(f"An error occurred: {error}")
        return {"error": str(error)}
