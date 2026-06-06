from datetime import datetime

from backend.database.collections import (
    chat_sessions_collection
)


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

    return str(result.inserted_id)