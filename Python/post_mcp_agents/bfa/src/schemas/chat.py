from pydantic import BaseModel


class ChatRequest(BaseModel):
    user: str
    message: str
