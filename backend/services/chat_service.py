from backend.services.predictor import predict_disease
from backend.services.symptom_extractor import extract_symptoms
from backend.services.recommendation_service import get_specialist

from backend.services.message_service import (
    create_message
)


def process_chat_message(
    session_id: str,
    content: str
):

    create_message(
        session_id=session_id,
        role="user",
        content=content
    )

    symptoms = extract_symptoms(content)

    prediction_result = predict_disease(content)

    disease = prediction_result["prediction"]

    specialist = get_specialist(disease)

    ai_response = f"""
Possible Disease: {disease}

Symptoms:
{', '.join(symptoms)}

Recommended Specialist:
{specialist}
"""

    create_message(
        session_id=session_id,
        role="assistant",
        content=ai_response
    )

    return {
        "prediction": disease,
        "symptoms": symptoms,
        "specialist": specialist,
        "response": ai_response,
        "top_predictions": prediction_result["top_predictions"]
    }