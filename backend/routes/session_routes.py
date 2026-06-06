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
    create_session,
    get_user_sessions
)

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)


@router.post(
    "/",
    summary="Create a chat session",
    description=(
        "Creates a new chat session for the authenticated user. "
        "Returns the generated session ID."
    )
)
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


@router.get(
    "/",
    summary="List user chat sessions",
    description=(
        "Returns all chat sessions belonging to the "
        "authenticated user, sorted by newest first."
    )
)
def get_sessions(
    current_user=Depends(get_current_user)
):

    return get_user_sessions(
        current_user["user_id"]
    )
