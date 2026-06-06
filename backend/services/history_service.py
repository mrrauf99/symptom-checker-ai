from datetime import datetime

from backend.database.collections import predictions_collection


def save_prediction(
    user_input,
    prediction,
    top_predictions
):

    predictions_collection.insert_one({
        "user_input": user_input,
        "prediction": prediction,
        "top_predictions": top_predictions,
        "created_at": datetime.utcnow()
    })