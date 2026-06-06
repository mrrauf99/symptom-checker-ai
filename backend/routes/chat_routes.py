from fastapi import APIRouter, Depends

from backend.auth.dependencies import (
    get_current_user
)

from backend.schemas.chat import ChatRequest

from backend.services.chat_service import (
    process_chat_message
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/send")
def send_message(
    data: ChatRequest,
    current_user=Depends(get_current_user)
):

    return process_chat_message(
        session_id=data.session_id,
        content=data.content
    )