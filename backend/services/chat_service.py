"""
Chat Service
============
Orchestrates the full chat message flow:
  1. Persist user message
  2. Extract symptoms from free-text input
  3. Predict disease using the ML model (with confidence + level)
  4. Fetch disease metadata (description, advice, specialist)
  5. Generate a rich formatted AI response
  6. Persist AI response
  7. Save prediction to history
  8. Return complete response payload

All existing response fields are preserved; confidence and confidence_level
are additive additions (backward compatible).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from backend.services.predictor import predict_disease
from backend.services.symptom_extractor import extract_symptoms
from backend.services.recommendation_service import get_specialist
from backend.services.disease_info_service import (
    get_disease_description,
    get_disease_advice,
)
from backend.services.message_service import create_message
from backend.services.history_service import save_prediction
from backend.utils.logger import logger


def process_chat_message(
    session_id: str,
    content: str,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Process a user chat message and return a structured AI response.

    Flow:
      1. Store user message
      2. Extract symptoms from the input
      3. Predict disease with confidence metadata
      4. Fetch disease description, advice, and specialist
      5. Generate a rich formatted response
      6. Store AI response
      7. Save prediction to history
      8. Return complete payload

    Args:
        session_id: Active chat session ID.
        content:    Raw message text from the user.
        user_id:    Authenticated user ID (optional).

    Returns:
        Dict containing prediction, symptoms, specialist, description,
        advice, confidence, confidence_level, response text, and
        top_predictions.
    """
    logger.info(f"Processing chat message for session {session_id}")

    # 1 — Store user message
    create_message(
        session_id=session_id,
        role="user",
        content=content
    )

    # 2 — Extract symptoms
    symptoms = extract_symptoms(content)
    logger.info(f"Symptoms extracted: {symptoms}")

    # 3 — Predict disease
    prediction_result = predict_disease(content)
    disease = prediction_result["prediction"]
    confidence = prediction_result["confidence"]
    confidence_level = prediction_result["confidence_level"]

    logger.info(
        f"Disease predicted: {disease} | "
        f"Confidence: {confidence}% ({confidence_level})"
    )

    # 4 — Fetch disease metadata
    specialist = get_specialist(disease)
    description = get_disease_description(disease)
    advice_list = get_disease_advice(disease)

    # 5 — Generate rich AI response
    ai_response = _generate_rich_response(
        disease=disease,
        confidence=confidence,
        confidence_level=confidence_level,
        symptoms=symptoms,
        description=description,
        specialist=specialist,
        advice_list=advice_list
    )

    # 6 — Store AI response
    create_message(
        session_id=session_id,
        role="assistant",
        content=ai_response,
        prediction_data={
            "prediction": disease,
            "confidence": confidence,
            "confidence_level": confidence_level,
            "symptoms": symptoms,
            "specialist": specialist,
            "description": description,
            "advice": advice_list,
            "top_predictions": prediction_result["top_predictions"]
        }
    )

    # 7 — Save prediction to history
    save_prediction(
        user_input=content,
        prediction=disease,
        top_predictions=prediction_result["top_predictions"],
        user_id=user_id
    )

    logger.info(f"Chat message processed successfully for session {session_id}")

    # 8 — Return complete payload
    return {
        "prediction": disease,
        "confidence": confidence,
        "confidence_level": confidence_level,
        "symptoms": symptoms,
        "specialist": specialist,
        "description": description,
        "advice": advice_list,
        "response": ai_response,
        "top_predictions": prediction_result["top_predictions"],
    }


def _generate_rich_response(
    disease: str,
    confidence: float,
    confidence_level: str,
    symptoms: List[str],
    description: str,
    specialist: str,
    advice_list: List[str]
) -> str:
    """
    Generate a formatted, human-readable AI response with full explanation.

    Includes: predicted disease, confidence score and level, detected
    symptoms, disease description, recommended specialist, and health advice.

    Args:
        disease:          Predicted disease name.
        confidence:       Numeric confidence percentage.
        confidence_level: "High" | "Medium" | "Low".
        symptoms:         List of canonical symptom names detected.
        description:      Disease description string.
        specialist:       Recommended medical specialist.
        advice_list:      List of health advice strings.

    Returns:
        Formatted multi-line response string.
    """
    symptoms_text = (
        "\n".join(f"• {s.capitalize()}" for s in symptoms)
        if symptoms
        else "• Unable to detect specific symptoms from the description"
    )
    advice_text = (
        "\n".join(f"• {advice}" for advice in advice_list)
        if advice_list
        else "• Consult with a qualified healthcare professional"
    )

    response = (
        f"Possible Disease: {disease}\n"
        f"\n"
        f"Confidence: {confidence}% ({confidence_level})\n"
        f"\n"
        f"Detected Symptoms:\n"
        f"{symptoms_text}\n"
        f"\n"
        f"About This Condition:\n"
        f"{description}\n"
        f"\n"
        f"Recommended Specialist:\n"
        f"{specialist}\n"
        f"\n"
        f"Health Advice:\n"
        f"{advice_text}\n"
        f"\n"
        f"Disclaimer:\n"
        f"This prediction is generated by an AI model and should not be "
        f"considered a medical diagnosis. Please consult a qualified "
        f"healthcare professional for proper evaluation and treatment."
    )

    return response