from datetime import datetime

from backend.database.collections import (
    chat_sessions_collection
)
from backend.utils.logger import logger


def create_session(
    user_id,
    title
):

    session = {
        "user_id": user_id,
        "title": title,
        "created_at": datetime.utcnow()
    }

    result = chat_sessions_collection.insert_one(
        session
    )

    session_id = str(result.inserted_id)

    logger.info(
        f"Session created: {session_id} for user {user_id}"
    )

    return session_id


def get_user_sessions(user_id):

    sessions = list(
        chat_sessions_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        )
        .sort("created_at", -1)
    )

    return sessions
