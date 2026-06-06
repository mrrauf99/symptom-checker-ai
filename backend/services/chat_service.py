from backend.services.predictor import (
    predict_disease
)

from backend.services.symptom_extractor import (
    extract_symptoms
)

from backend.services.recommendation_service import (
    get_specialist
)


def process_chat_message(text: str):

    symptoms = extract_symptoms(text)

    prediction_result = predict_disease(text)

    disease = prediction_result["prediction"]

    specialist = get_specialist(
        disease
    )

    response = f"""
Possible Disease: {disease}

Detected Symptoms:
{', '.join(symptoms)}

Recommended Specialist:
{specialist}
"""

    return {
        "prediction": disease,
        "symptoms": symptoms,
        "specialist": specialist,
        "response": response,
        "top_predictions": prediction_result[
            "top_predictions"
        ]
    }