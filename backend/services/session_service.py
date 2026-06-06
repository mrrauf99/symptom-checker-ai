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


def get_user_sessions(user_id):

    sessions = list(
        chat_sessions_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        )
        .sort("created_at", -1)
    )

    return sessions