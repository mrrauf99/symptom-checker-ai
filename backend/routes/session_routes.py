from fastapi import (
    APIRouter,
    Depends
)

from backend.schemas.session import (
    CreateSessionRequest
)

from backend.auth.dependencies import (
    get_current_user
)

from backend.services.session_service import (
    create_session
)

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)


@router.post("/")
def create_chat_session(
    data: CreateSessionRequest,
    current_user=Depends(get_current_user)
):

    session_id = create_session(
        current_user["user_id"],
        data.title
    )

    return {
        "session_id": session_id
    }