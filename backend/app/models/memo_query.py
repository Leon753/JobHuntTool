from pydantic import BaseModel

class MemoQuery(BaseModel):
    query: str
    response: str
