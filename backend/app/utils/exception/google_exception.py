import httpx

class GoogleSheetsAPIError(httpx.HTTPStatusError):
    """Custom exception for Google Sheets API errors."""
    def __init__(self, response: httpx.Response):
        super().__init__(f"Google Sheets API Error {response.status_code}: {response.text}", request=response.request, response=response)
