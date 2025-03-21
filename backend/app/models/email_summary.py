from pydantic import BaseModel
from enum import Enum

class Status(Enum):
    IN_REVIEW = "InReview"
    INTERVIEWING = "Interviewing"
    OFFER = "Offer"
    REJECTED = "Rejected"


class Email_Summary_Request(BaseModel):
    content: str

class GPT_Email_Summary_Response(BaseModel):
    summary: str
    company: str
    job_position: str
    status: Status

class GPT_SUMMARY_FEEDBACK(BaseModel):
    should_continue:bool
    feedback: str