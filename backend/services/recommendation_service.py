"""
Recommendation Service
======================
Provides specialist recommendation for a predicted disease.

Source of truth priority:
  1. disease_info.json (specialist field, loaded by disease_info_service)
  2. specialists.json  (fallback flat lookup)
  3. "General Physician" (final default)

The JSON file is loaded lazily and cached — no disk read on every call,
and no import-time crash if the file is missing.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional

from backend.utils.logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent
_SPECIALISTS_PATH = BASE_DIR / "data" / "specialists.json"

_specialists_cache: Optional[Dict[str, str]] = None


def _load_specialists() -> Dict[str, str]:
    """Load specialists.json once and cache in module-level variable."""
    global _specialists_cache

    if _specialists_cache is not None:
        return _specialists_cache

    try:
        with open(_SPECIALISTS_PATH, "r") as f:
            _specialists_cache = json.load(f)
        logger.info(
            f"Specialists lookup loaded: {len(_specialists_cache)} entries"
        )
    except FileNotFoundError:
        logger.warning(
            f"specialists.json not found at {_SPECIALISTS_PATH}. "
            "Falling back to General Physician for all diseases."
        )
        _specialists_cache = {}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing specialists.json: {e}")
        _specialists_cache = {}

    return _specialists_cache


def get_specialist(disease: str) -> str:
    """
    Return the recommended specialist for a predicted disease.

    Falls back to disease_info.json via disease_info_service if the disease
    is not in specialists.json, then to "General Physician" as a final default.

    Args:
        disease: Predicted disease name.

    Returns:
        Specialist name string.
    """
    # Primary lookup: disease_info.json (avoids data duplication)
    try:
        from backend.services.disease_info_service import get_disease_specialist
        specialist = get_disease_specialist(disease)
        if specialist and specialist != "General Physician":
            return specialist
    except Exception:
        pass

    # Secondary lookup: specialists.json flat file
    specialists = _load_specialists()
    return specialists.get(disease, "General Physician")