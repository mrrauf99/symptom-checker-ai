from datetime import datetime

from backend.database.collections import (
    chat_sessions_collection
)
from backend.utils.logger import logger
from bson.objectid import ObjectId


def create_session(
    user_id,
    title
):

    now = datetime.utcnow()
    session = {
        "user_id": user_id,
        "title": title,
        "status": "active",
        "created_at": now,
        "updated_at": now,
        "ended_at": None
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

    sessions = []
    for doc in chat_sessions_collection.find(
        {"user_id": user_id}
    ).sort("updated_at", -1):
        sessions.append({
            "id": str(doc["_id"]),
            "user_id": doc["user_id"],
            "title": doc["title"],
            "status": doc.get("status", "active"),
            "created_at": doc["created_at"].isoformat() + "Z" if isinstance(doc["created_at"], datetime) else doc["created_at"],
            "updated_at": doc.get("updated_at", doc["created_at"]).isoformat() + "Z" if isinstance(doc.get("updated_at", doc["created_at"]), datetime) else doc.get("updated_at", doc["created_at"]),
            "ended_at": doc.get("ended_at").isoformat() + "Z" if isinstance(doc.get("ended_at"), datetime) and doc.get("ended_at") else None
        })

    return sessions


def delete_session(session_id, user_id):
    """Delete a session only if it belongs to the current user"""
    try:
        object_id = ObjectId(session_id)
    except Exception as e:
        logger.error(f"Invalid session ID format: {session_id}")
        raise Exception("Invalid session ID format")
    
    try:
        result = chat_sessions_collection.delete_one({
            "_id": object_id,
            "user_id": user_id
        })
        
        if result.deleted_count == 0:
            raise Exception("Session not found or unauthorized")
        
        logger.info(f"Session deleted: {session_id} for user {user_id}")
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        raise


def get_session_by_id(session_id, user_id):
    """Retrieve a single session belonging to the user"""
    try:
        object_id = ObjectId(session_id)
    except Exception as e:
        logger.error(f"Invalid session ID format: {session_id}")
        raise Exception("Invalid session ID format")
    
    doc = chat_sessions_collection.find_one({
        "_id": object_id,
        "user_id": user_id
    })
    
    if not doc:
        return None
        
    return {
        "id": str(doc["_id"]),
        "user_id": doc["user_id"],
        "title": doc["title"],
        "status": doc.get("status", "active"),
        "created_at": doc["created_at"].isoformat() + "Z" if isinstance(doc["created_at"], datetime) else doc["created_at"],
        "updated_at": doc.get("updated_at", doc["created_at"]).isoformat() + "Z" if isinstance(doc.get("updated_at", doc["created_at"]), datetime) else doc.get("updated_at", doc["created_at"]),
        "ended_at": doc.get("ended_at").isoformat() + "Z" if isinstance(doc.get("ended_at"), datetime) and doc.get("ended_at") else None
    }


def end_session(session_id, user_id):
    """Mark a session as completed"""
    logger.info(f"end_session called with session_id={session_id}, user_id={user_id}")
    
    try:
        object_id = ObjectId(session_id)
        logger.info(f"Converted session_id to ObjectId: {object_id}")
    except Exception as e:
        logger.error(f"Invalid session ID format: {session_id}, error: {str(e)}")
        raise Exception("Invalid session ID format")
    
    # First check if session exists
    existing_session = chat_sessions_collection.find_one({"_id": object_id})
    logger.info(f"Existing session found: {existing_session is not None}")
    if existing_session:
        logger.info(f"Session user_id: {existing_session.get('user_id')}, current user_id: {user_id}")
    
    now = datetime.utcnow()
    result = chat_sessions_collection.update_one(
        {"_id": object_id, "user_id": user_id},
        {"$set": {
            "status": "completed",
            "updated_at": now,
            "ended_at": now
        }}
    )
    
    logger.info(f"Update result - matched_count: {result.matched_count}, modified_count: {result.modified_count}")
    
    if result.matched_count == 0:
        # Check if session exists at all
        session = chat_sessions_collection.find_one({"_id": object_id})
        if not session:
            logger.error(f"Session not found: {session_id}")
            raise Exception("Session not found")
        else:
            logger.error(f"User {user_id} not authorized to end session {session_id}. Session owner: {session.get('user_id')}")
            raise Exception("Not authorized to end this session")
        
    logger.info(f"Session {session_id} marked as completed for user {user_id}")
