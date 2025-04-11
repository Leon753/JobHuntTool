from pydantic import BaseModel
from typing import List, Dict, Union, Optional



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
    status: str  # Validated|Needs Work|Incorrect
    content: Union[List[str], str, int]  # bullet points, job title/location/type, or numeric score
    source: List[str]


class PayRangeContent(BaseModel):
    position: str
    salary: str


class PayRangeColumnResult(BaseModel):
    status: str
    content: List[PayRangeContent]
    source: List[str]


class Columns(BaseModel):
    job_description: ColumnResult
    interview_process: ColumnResult
    example_interview_experience: ColumnResult
    career_growth: ColumnResult
    example_technical_questions: ColumnResult
    years_of_experience: ColumnResult
    pay_range: PayRangeColumnResult

class JobInformation(BaseModel):
    company: str
    industry: str
    location: str
    score: str
    
    results: Columns
