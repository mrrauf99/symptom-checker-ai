from pydantic import BaseModel


class MessageRequest(BaseModel):
    session_id: str
    content: str