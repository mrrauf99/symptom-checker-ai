from datetime import datetime

from backend.database.collections import (
    messages_collection
)
from backend.utils.logger import logger


def create_message(
    session_id: str,
    role: str,
    content: str
):

    message = {
        "session_id": session_id,
        "role": role,
        "content": content,
        "created_at": datetime.utcnow()
    }

    result = messages_collection.insert_one(
        message
    )

    message_id = str(result.inserted_id)

    logger.info(
        f"Message stored: session {session_id}, role {role}"
    )

    return message_id


def get_session_messages(
    session_id: str
):

    messages = list(
        messages_collection.find(
            {
                "session_id": session_id
            },
            {
                "_id": 0
            }
        ).sort("created_at", 1)
    )

    return messages
