from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from backend.schemas.session import (
    CreateSessionRequest
)

from backend.auth.dependencies import (
    get_current_user
)

from backend.services.session_service import (
    create_session,
    get_user_sessions,
    delete_session,
    get_session_by_id,
    end_session
)

from backend.utils.logger import logger

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
    try:
        if isinstance(current_user, dict):
            user_id = current_user.get("user_id")
        else:
            user_id = getattr(current_user, "user_id", None)
        
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")

        session_id = create_session(
            user_id,
            data.title
        )

        return {
            "session_id": session_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


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
    try:
        if isinstance(current_user, dict):
            user_id = current_user.get("user_id")
        else:
            user_id = getattr(current_user, "user_id", None)
        
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")

        return get_user_sessions(
            user_id
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting sessions: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{session_id}",
    summary="Delete a chat session",
    description=(
        "Deletes a chat session belonging to the "
        "authenticated user."
    )
)
def delete_session_route(
    session_id: str,
    current_user=Depends(get_current_user)
):
    try:
        if isinstance(current_user, dict):
            user_id = current_user.get("user_id")
        else:
            user_id = getattr(current_user, "user_id", None)
        
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        delete_session(session_id, user_id)
        return {"message": "Session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{session_id}",
    summary="Get a specific chat session",
    description="Returns details for a specific chat session belonging to the authenticated user."
)
def get_session_route(
    session_id: str,
    current_user=Depends(get_current_user)
):
    try:
        if isinstance(current_user, dict):
            user_id = current_user.get("user_id")
        else:
            user_id = getattr(current_user, "user_id", None)
        
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        session = get_session_by_id(session_id, user_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session {session_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/{session_id}/end",
    summary="End a chat session",
    description="Marks a chat session as completed."
)
def end_session_route(
    session_id: str,
    current_user=Depends(get_current_user)
):
    try:
        logger.info(f"end_session_route called with session_id={session_id}")
        logger.info(f"current_user type: {type(current_user)}, value: {current_user}")
        
        if not current_user:
            logger.error("Current user is None")
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        if isinstance(current_user, dict):
            user_id = current_user.get("user_id")
            logger.info(f"Extracted user_id from dict: {user_id}")
        else:
            user_id = getattr(current_user, "user_id", None)
            logger.info(f"Extracted user_id from object: {user_id}")
        
        if not user_id:
            logger.error(f"user_id not found in current_user: {current_user}")
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        logger.info(f"Attempting to end session {session_id} for user {user_id}")
        end_session(session_id, user_id)
        logger.info(f"Successfully ended session {session_id}")
        return {"message": "Session ended successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to end session {session_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
