from pydantic import BaseModel
from typing import List, Dict


HEADER_COLUMNS = ["A", "B", "C", "D", "E", "F", "G"]
HEADER_NAMES = ["COMPANY", "JOB", "STATUS","JOB DESCRIPTION", "PAY RANGE", "INTERVIEW PROCESS", "EXAMPLE INTERVIEW EXPERIENCE"]


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


class Columns(BaseModel):
    job_description: ColumnResult
    pay_range: ColumnResult
    interview_process: ColumnResult
    example_interview_experience: ColumnResult

class JobInformation(BaseModel):
    company: str
    results: Columns