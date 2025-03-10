from pydantic import BaseModel
from typing import List, Dict



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