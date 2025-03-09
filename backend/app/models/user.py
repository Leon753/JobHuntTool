from pydantic import BaseModel

class UserAndExcelId(BaseModel):
    user_id: str
    excel_id: str

