from fastapi import (
    APIRouter,
    Depends
)

from backend.auth.dependencies import (
    get_current_user
)

from backend.schemas.message import (
    MessageRequest
)

from backend.services.message_service import (
    create_message,
    get_session_messages
)

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


@router.post(
    "/",
    summary="Store a chat message",
    description=(
        "Saves a user message to the specified chat session. "
        "Returns the generated message ID."
    )
)
def add_message(
    data: MessageRequest,
    current_user=Depends(get_current_user)
):

    message_id = create_message(
        session_id=data.session_id,
        role="user",
        content=data.content
    )

    return {
        "message_id": message_id,
        "message": "Message saved successfully"
    }


@router.get(
    "/{session_id}",
    summary="Get session messages",
    description=(
        "Returns all messages for a given chat session, "
        "ordered chronologically from oldest to newest."
    )
)
def get_messages(
    session_id: str,
    current_user=Depends(get_current_user)
):

    messages = get_session_messages(
        session_id
    )

    return messages
