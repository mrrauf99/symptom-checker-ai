from fastapi import APIRouter

from backend.schemas.prediction import PredictionRequest
from backend.services.predictor import predict_disease
from backend.services.history_service import save_prediction
from backend.database.mongodb import predictions_collection

router = APIRouter()


@router.post("/predict")
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


@router.get("/history")
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


@router.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Healthcare Symptom Checker API"
    }