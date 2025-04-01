from pydantic import BaseModel
from typing import List, Dict

# Archive for LLM Query Calls 
class DataItem(BaseModel):
    range: str
    majorDimension: str
    values: List[List[str]]

class GoogleSheetsData(BaseModel):
    valueInputOption: str
    data: List[DataItem]
    includeValuesInResponse: bool
    responseValueRenderOption: str
    responseDateTimeRenderOption: str

class TableRowRequestPayload(BaseModel):
    user_id:str 
    email_content:str

    

class ColumnResult(BaseModel):
    status: str
    content: List[str]
    source: List[str]

class PayRange_ColumnResult(BaseModel):
    status: str
    content: List[Dict[str, str]]
    source: List[str]

class Columns(BaseModel):
    job_description: ColumnResult
    pay_range: PayRange_ColumnResult
    interview_process: ColumnResult
    example_interview_experience: ColumnResult
    career_growth: ColumnResult
    example_technical_questions: ColumnResult


class JobInformation(BaseModel):
    company: str
    results: Columns