from pydantic import BaseModel
from typing import List, Dict

class ColumnResult(BaseModel):
    status: str
    content: str
    source: List[str]

class JobInformation(BaseModel):
    company: str
    results: Dict[str, ColumnResult]