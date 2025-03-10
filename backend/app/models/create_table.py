from pydantic import BaseModel
from typing import List, Dict


HEADER_COLUMNS = ["B", "C", "D", "E", "F", "G", "H"]
HEADER_NAMES = ["COMPANY", "JOB", "STATUS","JOB DESCRIPTION", "PAY RANGE", "INTERVIEW PROCESS", "EXAMPLE INTERVIEW EXPERIENCE"]
HEADER_TO_COLUMN = {
    HEADER_NAMES[0]: HEADER_COLUMNS[0],
    HEADER_NAMES[1]: HEADER_COLUMNS[1],
    HEADER_NAMES[2]: HEADER_COLUMNS[2],
    HEADER_NAMES[3]: HEADER_COLUMNS[3],
    HEADER_NAMES[4]: HEADER_COLUMNS[4],
    HEADER_NAMES[5]: HEADER_COLUMNS[5] ,
    HEADER_NAMES[6]: HEADER_COLUMNS[6]
}
HEADER_TO_INDEX = {
    HEADER_NAMES[0]: 0,
    HEADER_NAMES[1]: 1,
    HEADER_NAMES[2]: 2,
    HEADER_NAMES[3]: 3,
    HEADER_NAMES[4]: 4,
    HEADER_NAMES[5]: 5 ,
    HEADER_NAMES[6]: 6
}




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
    sheets_data:GoogleSheetsData
    

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