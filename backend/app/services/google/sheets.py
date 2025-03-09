import requests 

def createSheet(headers: dict, body: dict) -> dict:
    try:
        auth_header = headers.get("authorization")
        if not auth_header:
            raise ValueError("Missing authorization header")
        
        headerValues = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
        }
        response = requests.post("https://sheets.googleapis.com/v4/spreadsheets", headers=headerValues, json=body)
        if response.status_code == 200:
            print(response)
            return response.json()
        
        return {"error": f"Unexpected status {response.status_code}", "details": response.text}
    except Exception as error:
        print(f"An error occurred: {error}")
        return {"error": str(error)}



# const response = await fetch(
#           `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values:batchUpdate`,
#           {
#               method: "POST",
#               headers: {
#                   "Content-Type": "application/json",
#                   Authorization: `Bearer ${token}`
#               },
#               body: JSON.stringify(requestBody)
#           }
#       );

def updateSheet(headers: dict, body: dict, spreadsheetId: str) -> dict:
    try:
        auth_header = headers.get("authorization")
        if not auth_header:
            raise ValueError("Missing authorization header")
        
        headerValues = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
        }
        response = requests.post(f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values:batchUpdate", headers=headerValues, json=body)
        if response.status_code == 200:
            print(response)
            return response.json()
        
        return {"error": f"Unexpected status {response.status_code}", "details": response.text}
    except Exception as error:
        print(f"An error occurred: {error}")
        return {"error": str(error)}
