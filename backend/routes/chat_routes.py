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

from backend.services.chat_service import (
    process_chat_message
)

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)


@router.post("/")
def chat(
    data: MessageRequest,
    current_user=Depends(
        get_current_user
    )
):

    result = process_chat_message(
        data.content
    )

    return result