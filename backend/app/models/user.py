from pydantic import BaseModel

class UserAndExcelId(BaseModel):
    user_id: str
    current_sheet_row: int
    excel_id: str

