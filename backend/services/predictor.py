"""
Disease Prediction Service
==========================
Loads the trained sklearn Pipeline once at startup (module-level singleton)
and exposes a single public function: predict_disease().

Confidence levels:
  >= 70  → High
  >= 40  → Medium
  <  40  → Low

Response fields (all backward-compatible):
  prediction        str   — top predicted disease
  confidence        float — confidence % of top prediction
  confidence_level  str   — "High" | "Medium" | "Low"
  top_predictions   list  — top-3 dicts with disease, confidence, confidence_level
  symptoms          list  — canonical symptom names extracted from the input text
  specialist        str   — recommended medical specialist for the predicted disease

Changelog (v3):
  - Added symptom-based boosting layer: adjusts ML probabilities based on
    extracted symptom patterns to bridge the gap between terse user input
    and the model's training distribution.
  - Boosting is a lightweight ranking adjustment, NOT a hardcoded override.
  - All existing fields and API contracts are preserved (backward compatible).

Changelog (v2):
  - predict_disease() now returns "symptoms" and "specialist" fields.
    These are additive (backward-compatible): no existing field was modified.
  - Imports extract_symptoms and get_specialist lazily to avoid circular imports.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import numpy as np
import joblib

from backend.utils.logger import logger

# ---------------------------------------------------------------------------
# Model — loaded once at startup (module-level singleton)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "models" / "disease_model.pkl"

try:
    _model = joblib.load(MODEL_PATH)
    logger.info(f"Disease prediction model loaded from {MODEL_PATH}")
except Exception as e:
    logger.error(f"Failed to load disease model: {str(e)}")
    _model: Optional[Any] = None


# ---------------------------------------------------------------------------
# Symptom-based boosting rules
# ---------------------------------------------------------------------------
# Each rule maps a disease to:
#   "required"  — if ALL present, apply full boost
#   "partial"   — if >= partial_threshold match, apply partial boost
#   "boost"     — probability mass added for full match (before re-norm)
#   "partial_boost" — for partial match
#   "dampen"    — dict of {disease: amount} to REDUCE when this rule fires.
#                  This handles confusion pairs (e.g. Pneumonia evidence → dampen Asthma)

_BOOST_RULES: List[Dict[str, Any]] = [
    {
        "disease": "Bronchial Asthma",
        "required": {"wheezing"},
        "partial": {"chest tightness", "shortness of breath", "cough"},
        "partial_threshold": 2,
        "boost": 0.25,
        "partial_boost": 0.12,
        "dampen": {},
    },
    {
        "disease": "Pneumonia",
        "required": {"productive cough"},
        "partial": {"chest pain", "fever", "chest congestion", "chills",
                     "shortness of breath"},
        "partial_threshold": 2,
        "boost": 0.30,
        "partial_boost": 0.12,
        # When productive cough is present, asthma is unlikely (asthma = dry/wheezy)
        "dampen": {"Bronchial Asthma": 0.65},
    },
    {
        "disease": "Chicken pox",
        "required": {"blisters"},
        "partial": {"rash", "itching", "fever"},
        "partial_threshold": 1,
        "boost": 0.25,
        "partial_boost": 0.12,
        # Blisters = vesicles (chickenpox), not sores (impetigo)
        "dampen": {"Impetigo": 0.30},
    },
    {
        "disease": "Malaria",
        "required": {"chills", "sweating"},
        "partial": {"fever", "headache", "vomiting", "muscle pain"},
        "partial_threshold": 2,
        "boost": 0.22,
        "partial_boost": 0.10,
        # Chills + sweating is classic malaria, not typhoid (which is GI-dominant)
        "dampen": {"Typhoid": 0.20},
    },
    {
        "disease": "Dengue",
        "required": {"pain behind eyes"},
        "partial": {"fever", "headache", "rash", "joint pain", "muscle pain"},
        "partial_threshold": 2,
        "boost": 0.18,
        "partial_boost": 0.10,
        "dampen": {},
    },
    {
        "disease": "Typhoid",
        "required": {"loss of appetite"},
        "partial": {"fever", "abdominal pain", "diarrhea", "fatigue"},
        "partial_threshold": 2,
        "boost": 0.15,
        "partial_boost": 0.08,
        "dampen": {},
    },
    {
        "disease": "Arthritis",
        "required": {"joint pain"},
        "partial": {"fatigue"},
        "partial_threshold": 1,
        "boost": 0.30,
        "partial_boost": 0.15,
        # Joint pain without skin symptoms → dampen Psoriasis
        "dampen": {"Psoriasis": 0.60},
    },
    {
        "disease": "Psoriasis",
        "required": {"silvery scales"},
        "partial": {"rash", "itching"},
        "partial_threshold": 1,
        "boost": 0.18,
        "partial_boost": 0.10,
        "dampen": {},
    },
]


def _apply_symptom_boost(
    probabilities: np.ndarray,
    classes: np.ndarray,
    symptoms: List[str],
) -> np.ndarray:
    """
    Apply symptom-based boosting to ML probabilities.

    This is a lightweight ranking adjustment — it adds probability mass to
    diseases whose clinical symptom patterns are detected, and optionally
    dampens confused diseases. Then re-normalizes so probabilities sum to 1.0.

    Args:
        probabilities: Raw probability array from the model (shape: [n_classes]).
        classes: Array of class labels (shape: [n_classes]).
        symptoms: List of canonical symptom names extracted from user input.

    Returns:
        Adjusted probability array (same shape, sums to 1.0).
    """
    if not symptoms:
        return probabilities

    adjusted = probabilities.copy()
    symptom_set: Set[str] = set(symptoms)
    class_to_idx = {c: i for i, c in enumerate(classes)}

    for rule in _BOOST_RULES:
        disease = rule["disease"]
        if disease not in class_to_idx:
            continue

        idx = class_to_idx[disease]
        required = rule["required"]
        partial = rule["partial"]
        threshold = rule["partial_threshold"]

        # Check required symptoms
        required_match = required.issubset(symptom_set)
        partial_matches = len(partial.intersection(symptom_set))

        if required_match and partial_matches >= threshold:
            # Full boost: strong clinical evidence
            adjusted[idx] += rule["boost"]

            # Dampen confused diseases
            for dampen_disease, dampen_amount in rule.get("dampen", {}).items():
                if dampen_disease in class_to_idx:
                    didx = class_to_idx[dampen_disease]
                    adjusted[didx] *= (1.0 - dampen_amount)

            logger.debug(
                f"Boost +{rule['boost']:.2f} for {disease} "
                f"(required={required}, partial_matches={partial_matches})"
            )
        elif required_match or partial_matches >= threshold:
            # Partial boost: some evidence present
            adjusted[idx] += rule["partial_boost"]

            # Apply half dampening for partial matches
            for dampen_disease, dampen_amount in rule.get("dampen", {}).items():
                if dampen_disease in class_to_idx:
                    didx = class_to_idx[dampen_disease]
                    adjusted[didx] *= (1.0 - dampen_amount * 0.5)

            logger.debug(
                f"Partial boost +{rule['partial_boost']:.2f} for {disease} "
                f"(required_match={required_match}, partial_matches={partial_matches})"
            )

    # Ensure no negative values
    adjusted = np.maximum(adjusted, 0.0)

    # Re-normalize to sum to 1.0
    total = adjusted.sum()
    if total > 0:
        adjusted /= total

    return adjusted


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_confidence_level(confidence: float) -> str:
    """
    Convert a numeric confidence percentage to a human-readable label.

    Thresholds:
        >= 70  → "High"
        >= 40  → "Medium"
        <  40  → "Low"

    Args:
        confidence: Confidence score as a percentage (0–100).

    Returns:
        Confidence level label string.
    """
    if confidence >= 70:
        return "High"
    elif confidence >= 40:
        return "Medium"
    return "Low"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def predict_disease(text: str) -> Dict[str, Any]:
    """
    Predict disease from a free-text symptom description.

    Pipeline:
      1. ML model predicts class probabilities from raw text.
      2. Symptom extractor identifies canonical symptoms from the text.
      3. Symptom-based boosting adjusts probabilities using clinical rules.
      4. Top prediction, confidence, and metadata are assembled.

    All existing response fields are preserved (backward compatible).
    The boosting layer is additive — it nudges probabilities, never overrides.

    Args:
        text: Raw patient symptom description.

    Returns:
        {
            "prediction":        str   — top predicted disease,
            "confidence":        float — confidence % of top prediction,
            "confidence_level":  str   — "High" | "Medium" | "Low",
            "top_predictions":   list  — top-3 dicts with disease,
                                         confidence, confidence_level,
            "symptoms":          list  — canonical symptom names found in text,
            "specialist":        str   — recommended specialist for prediction,
        }

    Raises:
        RuntimeError: If the model failed to load at startup.
    """
    if _model is None:
        logger.error("Model not available for prediction")
        raise RuntimeError("Prediction model failed to load")

    # --- Symptom extraction (before ML, needed for boosting) ---
    try:
        from backend.services.symptom_extractor import extract_symptoms
        symptoms: List[str] = extract_symptoms(text)
    except Exception as exc:
        logger.warning(f"Symptom extraction failed: {exc}")
        symptoms = []

    # --- Core ML prediction ---
    raw_probabilities = _model.predict_proba([text])[0]
    classes = _model.classes_

    # --- Symptom-based boosting ---
    adjusted_probabilities = _apply_symptom_boost(
        raw_probabilities, classes, symptoms
    )

    # Build full ranked list from adjusted probabilities
    all_results: List[Dict[str, Any]] = []
    for disease, score in zip(classes, adjusted_probabilities):
        conf = round(float(score * 100), 2)
        all_results.append({
            "disease": disease,
            "confidence": conf,
            "confidence_level": get_confidence_level(conf),
        })

    all_results.sort(key=lambda x: x["confidence"], reverse=True)
    top_3 = all_results[:3]

    prediction = top_3[0]["disease"]
    top_confidence = top_3[0]["confidence"]
    top_confidence_level = top_3[0]["confidence_level"]

    # --- Specialist lookup (lazy import) ---
    try:
        from backend.services.recommendation_service import get_specialist
        specialist: str = get_specialist(prediction)
    except Exception as exc:
        logger.warning(f"Specialist lookup failed: {exc}")
        specialist = "General Physician"

    logger.info(
        f"Prediction: {prediction} | "
        f"Confidence: {top_confidence}% ({top_confidence_level}) | "
        f"Symptoms: {symptoms} | "
        f"Specialist: {specialist}"
    )

    return {
        "prediction":       prediction,
        "confidence":       top_confidence,
        "confidence_level": top_confidence_level,
        "top_predictions":  top_3,
        "symptoms":         symptoms,
        "specialist":       specialist,
    }

