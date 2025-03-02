from pydantic import BaseModel

class Email_Summary_Request(BaseModel):
    content: str