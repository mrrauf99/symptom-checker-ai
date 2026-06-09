"""
ML Text Preprocessing Utilities
================================
Shared text normalization functions used by both:
  - ml/train.py  (at training time)
  - models/disease_model.pkl  (FunctionTransformer references this module)

IMPORTANT: This module must be importable from the same Python path used by
both the training script and the production backend. It is referenced by the
saved sklearn pipeline via FunctionTransformer, so the function name and
module path must remain stable across versions.

Functions:
  preprocess_text(texts) — normalises raw symptom text before TF-IDF vectorisation.

Changelog (v2):
  - Added _PHRASE_MAP: known medical phrases are preserved as underscore-joined
    tokens before hyphen normalization. This prevents TF-IDF from splitting
    "fluid-filled blisters" into disconnected unigrams.
  - Added punctuation normalization: strips sentence-ending punctuation so
    "Fever." and "Fever" produce identical tokens.
  - Lowercasing applied for consistent matching.
"""

from __future__ import annotations

import re
from typing import Union

import pandas as pd


# ---------------------------------------------------------------------------
# Phrase preservation map
# ---------------------------------------------------------------------------
# These multi-word medical phrases are joined with underscores BEFORE hyphen
# normalization so that TF-IDF treats them as single features.
# Sorted longest-first to avoid partial matches.
_PHRASE_MAP = [
    ("fluid-filled blisters", "fluid_filled_blisters"),
    ("fluid filled blisters", "fluid_filled_blisters"),
    ("pain behind the eyes", "pain_behind_eyes"),
    ("pain behind my eyes", "pain_behind_eyes"),
    ("pain behind eyes", "pain_behind_eyes"),
    ("shortness of breath", "shortness_of_breath"),
    ("difficulty breathing", "difficulty_breathing"),
    ("loss of appetite", "loss_of_appetite"),
    ("chest tightness", "chest_tightness"),
    ("chest congestion", "chest_congestion"),
    ("chest pain", "chest_pain"),
    ("joint pain", "joint_pain"),
    ("muscle pain", "muscle_pain"),
    ("body aches", "body_aches"),
    ("cough producing mucus", "productive_cough"),
    ("cough with mucus", "productive_cough"),
    ("cough with phlegm", "productive_cough"),
    ("productive cough", "productive_cough"),
    ("dry cough", "dry_cough"),
    ("high fever", "high_fever"),
    ("skin rash", "skin_rash"),
]


def _normalize_single(text: str) -> str:
    """
    Normalise a single symptom text string.

    Steps:
      1. Lowercase for consistent matching.
      2. Preserve known medical phrases as underscore-joined tokens.
      3. Convert remaining hyphens to spaces (e.g. "run-down" → "run down").
      4. Remove sentence-ending punctuation that fragments tokens.
      5. Collapse consecutive whitespace.
      6. Strip leading/trailing whitespace.
    """
    t = text.lower()

    # Preserve known phrases
    for phrase, token in _PHRASE_MAP:
        t = t.replace(phrase, token)

    # Hyphens → spaces (for remaining hyphenated words)
    t = t.replace("-", " ")

    # Strip punctuation that fragments tokens (keep underscores)
    t = re.sub(r"[.,;:!?\"'()\[\]{}]", " ", t)

    # Collapse whitespace
    t = re.sub(r"\s+", " ", t).strip()

    return t


def preprocess_text(texts: Union[pd.Series, list]) -> Union[pd.Series, list]:
    """
    Normalise raw symptom text before vectorisation.

    Operations:
      1. Lowercase for consistent matching.
      2. Preserve known medical phrases as underscore-joined tokens:
         "fluid-filled blisters" → "fluid_filled_blisters"
         This ensures TF-IDF captures these as single features, improving
         separation of diseases with overlapping vocabulary.
      3. Convert remaining hyphens to spaces:
         "run-down" → "run down"
      4. Remove sentence-ending punctuation.
      5. Collapse consecutive whitespace.
      6. Strip leading/trailing whitespace.

    Args:
        texts: pandas Series or list of strings.

    Returns:
        pandas Series or list with normalised strings (same type as input).
    """
    if isinstance(texts, pd.Series):
        return texts.apply(_normalize_single)
    return [_normalize_single(t) for t in texts]

