from datetime import datetime

from backend.database.collections import predictions_collection
from backend.utils.logger import logger


def save_prediction(
    user_input,
    prediction,
    top_predictions,
    user_id=None
):
    """Save prediction record to history for tracking and analysis"""

    doc = {
        "user_input": user_input,
        "prediction": prediction,
        "top_predictions": top_predictions,
        "created_at": datetime.utcnow()
    }

    if user_id:
        doc["user_id"] = user_id

    predictions_collection.insert_one(doc)
    
    logger.info(
        f"Prediction saved - disease: {prediction}, "
        f"user: {user_id or 'anonymous'}"
    )


def get_user_predictions(user_id, limit=20):
    """Retrieve user's prediction history"""

    predictions = list(
        predictions_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        )
        .sort("created_at", -1)
        .limit(limit)
    )
    
    logger.info(
        f"Retrieved {len(predictions)} predictions for user {user_id}"
    )

    return predictions