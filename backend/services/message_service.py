from datetime import datetime

from backend.database.collections import (
    messages_collection
)
from backend.utils.logger import logger


def create_message(
    session_id: str,
    role: str,
    content: str,
    prediction_data: dict = None
):
    """Store a message in the chat session"""

    message = {
        "session_id": session_id,
        "role": role,
        "content": content,
        "created_at": datetime.utcnow()
    }
    
    if prediction_data:
        message["prediction_data"] = prediction_data

    result = messages_collection.insert_one(
        message
    )

    from backend.database.collections import chat_sessions_collection
    from bson.objectid import ObjectId
    chat_sessions_collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"updated_at": message["created_at"]}}
    )

    message_id = str(result.inserted_id)

    content_preview = content[:50] + "..." if len(content) > 50 else content
    logger.info(
        f"Message stored - session: {session_id}, role: {role}, "
        f"preview: {content_preview}"
    )

    return message_id


def get_session_messages(
    session_id: str
):
    """Retrieve all messages for a session sorted by creation time"""

    messages = list(
        messages_collection.find(
            {
                "session_id": session_id
            }
        ).sort("created_at", 1)
    )
    
    # Format messages for response
    formatted_messages = []
    for msg in messages:
        formatted_msg = {
            "role": msg.get("role"),
            "content": msg.get("content")
        }
        if "prediction_data" in msg:
            formatted_msg["prediction_data"] = msg["prediction_data"]
        formatted_messages.append(formatted_msg)

    logger.info(f"Retrieved {len(formatted_messages)} messages for session {session_id}")

    return formatted_messages
