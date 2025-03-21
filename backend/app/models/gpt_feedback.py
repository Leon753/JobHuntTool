from pydantic import BaseModel

class GPT_SUMMARY_FEEDBACK(BaseModel):
    should_continue:bool
    feedback: str
    summary_rating: int