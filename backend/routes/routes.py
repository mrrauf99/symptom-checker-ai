from fastapi import APIRouter

from backend.schemas.prediction import PredictionRequest
from backend.services.predictor import predict_disease
from backend.services.history_service import save_prediction
from backend.database.collections import predictions_collection

router = APIRouter()


@router.post(
    "/predict",
    summary="Predict disease from symptoms",
    description=(
        "Accepts a free-text symptom description and returns "
        "the predicted disease with top confidence scores. "
        "The result is saved to prediction history."
    ),
    tags=["Prediction"]
)
def predict(data: PredictionRequest):

    result = predict_disease(data.text)

    save_prediction(
        user_input=data.text,
        prediction=result["prediction"],
        top_predictions=result["top_predictions"]
    )

    return {
        "input": data.text,
        "prediction": result["prediction"],
        "top_predictions": result["top_predictions"]
    }


@router.get(
    "/history",
    summary="Get recent prediction history",
    description=(
        "Returns the 20 most recent disease predictions "
        "stored in the database, sorted by newest first."
    ),
    tags=["History"]
)
def history():

    records = list(
        predictions_collection.find(
            {},
            {"_id": 0}
        )
        .sort("created_at", -1)
        .limit(20)
    )

    return records


@router.get(
    "/health",
    summary="Health check",
    description=(
        "Returns the current health status of the API. "
        "Use this endpoint for uptime monitoring and load balancer checks."
    ),
    tags=["Health"]
)
def health_check():

    return {
        "status": "healthy",
        "service": "Healthcare Symptom Checker API",
        "version": "1.0.0"
    }


@router.get(
    "/version",
    summary="Get API version",
    description="Returns the application name and current version number.",
    tags=["Health"]
)
def version():

    return {
        "name": "Healthcare Symptom Checker",
        "version": "1.0.0"
    }
