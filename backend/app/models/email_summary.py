from pydantic import BaseModel

class Email_Summary_Request(BaseModel):
    content: str

class GPT_Email_Summary_Response(BaseModel):
    summary: str
    company: str
    job_position: str