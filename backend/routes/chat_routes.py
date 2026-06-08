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


@router.post(
    "/send",
    summary="Send a chat message",
    description=(
        "Sends a message within a chat session. The system extracts "
        "symptoms, runs disease prediction, recommends a specialist, "
        "and stores both the user message and AI response."
    )
)
def send_message(
    data: ChatRequest,
    current_user=Depends(get_current_user)
):

    return process_chat_message(
        session_id=data.session_id,
        content=data.content,
        user_id=current_user["user_id"]
    )
