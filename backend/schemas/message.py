from pydantic import BaseModel


class MessageRequest(BaseModel):
    session_id: str
    content: str


class MessageResponse(BaseModel):
    session_id: str
    role: str
    content: str