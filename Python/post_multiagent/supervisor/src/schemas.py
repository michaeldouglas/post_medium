from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_id: str
    client_id: str
