"""
Symptom Extractor Service
=========================
Extracts canonical symptom names from free-text patient descriptions using
a centralized symptom knowledge base with regex word-boundary matching.

Each key is the canonical symptom name returned to callers.
Each value list contains all alias phrases that map to that canonical name.
Aliases are sorted longest-first so that multi-word phrases (e.g. "high fever")
match before shorter overlapping ones (e.g. "fever").
The module-level SYMPTOM_SYNONYMS constant is compiled once at import time.
"""

from __future__ import annotations

import re
from typing import Dict, List, Set, Tuple

# ---------------------------------------------------------------------------
# Canonical symptom → synonym aliases
# (Centralised knowledge base — single source of truth)
# ---------------------------------------------------------------------------
SYMPTOM_SYNONYMS: Dict[str, List[str]] = {

    # ------------------------------------------------------------------ fever
    "fever": [
        "high fever", "fever", "feverish", "pyrexia",
        "temperature", "running a temperature", "febrile",
        "elevated temperature", "low-grade fever", "mild fever",
    ],

    # --------------------------------------------------------- recurring fever
    # Malaria differentiator — cyclical/recurring fever patterns distinguish
    # malaria from dengue (sudden sustained) and typhoid (step-ladder).
    "recurring fever": [
        "recurring fever", "recurrent fever", "cyclical fever",
        "periodic fever", "fever comes and goes", "intermittent fever",
        "fever that comes back", "episodic fever", "fever episodes",
        "recurring episodes of fever", "recurring episodes of high fever",
        "sweating episodes",
    ],

    # ----------------------------------------------------------------- chills
    "chills": [
        "chills", "chilling", "chill", "shivering",
        "rigors", "rigor", "shakes", "cold shakes",
    ],

    # --------------------------------------------------------------- sweating
    "sweating": [
        "excessive sweating", "sweating", "sweats", "sweat",
        "night sweats", "perspiration", "perspiring", "drenched in sweat",
    ],

    # ---------------------------------------------------------------- fatigue
    "fatigue": [
        "exhaustion", "exhausted", "extreme exhaustion",
        "fatigue", "fatigued", "weakness", "weak", "weakened",
        "tired", "tiredness", "lethargy", "lethargic",
        "low energy", "no energy", "lack of energy",
        "feeling drained", "drained", "run-down",
    ],

    # --------------------------------------------------------------- headache
    "headache": [
        "headache", "headaches", "head ache", "head pain",
        "migraine", "migraines", "pounding head",
        "throbbing head", "severe headache",
    ],

    # ---------------------------------------------------- pain behind eyes
    # Dengue differentiator — retro-orbital pain distinguishes dengue from malaria/typhoid
    "pain behind eyes": [
        "pain behind eyes", "pain behind the eyes",
        "pain behind my eyes", "pain around my eyes",
        "retro-orbital pain", "retroorbital pain",
        "pain around the eyes", "pain around eyes",
        "eye pain", "aching behind the eyes",
        "aching behind my eyes",
    ],

    # -------------------------------------------------------------- muscle pain
    "muscle pain": [
        "muscle pain", "muscle ache", "muscle aches", "myalgia",
        "body pain", "body ache", "body aches", "body soreness",
        "muscular pain", "sore muscles", "muscle soreness",
        "aching muscles", "muscles are aching", "aching body",
        "aches all over", "aches and pains",
    ],

    # --------------------------------------------------------------- joint pain
    "joint pain": [
        "joint pain", "joint ache", "joint aches", "arthralgia",
        "painful joints", "stiff joints", "joint stiffness",
        "swollen joints", "joint swelling", "aching joints",
        "joints are stiff", "joints are swollen",
        "morning stiffness", "stiffness in joints",
        "joints feel stiff", "joint inflammation",
    ],

    # ----------------------------------------------------------------- nausea
    "nausea": [
        "nausea", "nauseous", "feel sick", "feeling sick",
        "queasy", "queasiness", "stomach upset",
        "sick to my stomach", "unsettled stomach",
    ],

    # --------------------------------------------------------------- vomiting
    "vomiting": [
        "vomiting", "vomit", "throwing up", "throw up",
        "threw up", "puked", "puke", "retching",
        "retch", "emesis", "feeling like vomiting",
    ],

    # ------------------------------------------------------------------ cough
    # NOTE: productive/mucus cough aliases moved to dedicated "productive cough"
    # canonical below to disambiguate Pneumonia (productive) from Asthma (dry).
    "cough": [
        "cough", "coughing", "dry cough", "wet cough",
        "persistent cough", "chronic cough", "hacking cough",
    ],

    # -------------------------------------------------------- productive cough
    # Pneumonia differentiator — productive cough with mucus/phlegm indicates
    # lower respiratory infection, NOT bronchial asthma (which is dry/wheezy).
    "productive cough": [
        "productive cough", "cough producing mucus", "cough with mucus",
        "cough with phlegm", "coughing up mucus", "coughing up phlegm",
        "phlegm cough", "mucus cough", "mucus production",
        "cough producing phlegm", "bringing up mucus", "bringing up phlegm",
    ],

    # -------------------------------------------------------- shortness of breath
    # NOTE: "wheezing" removed — now a separate canonical (Asthma differentiator)
    "shortness of breath": [
        "shortness of breath", "short of breath",
        "difficulty breathing", "breathing difficulty",
        "breathlessness", "breathless", "labored breathing",
        "struggling to breathe", "can't breathe", "cannot breathe",
        "respiratory distress",
    ],

    # --------------------------------------------------------------- wheezing
    # Asthma differentiator — wheezing (whistling sound on expiration) is the
    # hallmark symptom of bronchial asthma, distinct from general breathlessness.
    "wheezing": [
        "wheezing", "wheeze", "wheezy",
        "whistling breathing", "whistling sound when breathing",
        "whistling breath", "breathing whistles",
    ],

    # --------------------------------------------------------------- chest pain
    # NOTE: "chest tightness" / "tight chest" removed — now a separate canonical
    # (Asthma differentiator). Chest pain = sharp/aching pain (Pneumonia, cardiac).
    "chest pain": [
        "chest pain", "chest ache",
        "chest discomfort", "chest pressure",
        "pain in chest", "painful breathing",
        "chest pain when breathing", "pain when breathing",
    ],

    # --------------------------------------------------------- chest tightness
    # Asthma differentiator — chest tightness (constriction) is characteristic
    # of bronchial asthma, distinct from sharp chest pain (pneumonia/cardiac).
    "chest tightness": [
        "chest tightness", "tight chest", "tightness in chest",
        "chest feels tight", "constricted chest", "chest constriction",
    ],

    # -------------------------------------------------------- chest congestion
    # Pneumonia differentiator — distinguishes from bronchial asthma (which presents
    # with wheezing/breathlessness rather than true productive congestion)
    "chest congestion": [
        "chest congestion", "congested chest",
        "chest feels congested", "chest fullness",
        "chest feels full", "congestion in chest",
        "mucus in chest", "phlegm in chest",
        "mucus in my chest", "phlegm in my chest",
        "congestion in my chest",
    ],

    # ------------------------------------------------------------------- rash
    # NOTE: "blisters" / "blister" removed from this list — they now map to the
    # dedicated "blisters" canonical below to disambiguate Chicken Pox from
    # Impetigo / Psoriasis (which present with sores / scaly patches, not true vesicles).
    "rash": [
        "rash", "skin rash", "hives", "urticaria",
        "skin eruption", "eruption", "red spots",
        "skin lesions", "scaly patches", "scaly skin", "scaling skin",
        "skin peeling", "peeling skin", "red patches",
    ],

    # --------------------------------------------------------------- blisters
    # Chicken Pox differentiator — varicella produces fluid-filled vesicles;
    # Impetigo produces pus-filled sores; keeping these separate improves
    # the model's ability to distinguish the two diseases.
    "blisters": [
        "fluid-filled blisters", "fluid filled blisters",
        "water blisters", "vesicles", "skin blisters",
        "blistering", "blister", "blisters",
        "fluid filled lesions", "fluid-filled lesions",
        "itchy blisters", "itching blisters",
    ],

    # ----------------------------------------------------------- silvery scales
    # Psoriasis differentiator — the "silver-like dusting" description appears
    # in the Psoriasis training set and is a clinically distinctive feature.
    "silvery scales": [
        "silvery scales", "silver scales",
        "silver-like dusting", "silver like dusting",
        "scaly plaques", "silver dusting", "silvery plaques",
        "silver scaly patches",
        "flaky patches", "scaling skin", "flaky skin",
    ],

    # --------------------------------------------------------------- itching
    "itching": [
        "itching", "itchy", "itch", "pruritus",
        "skin itching", "itchy skin", "intense itching",
    ],

    # --------------------------------------------------------------- diarrhea
    "diarrhea": [
        "diarrhea", "diarrhoea", "loose stools", "loose motions",
        "watery stools", "frequent stools", "runny stool",
    ],

    # --------------------------------------------------------- loss of appetite
    "loss of appetite": [
        "loss of appetite", "no appetite", "poor appetite",
        "not hungry", "decreased appetite",
        "reduced appetite", "not eating", "unable to eat",
    ],

    # ---------------------------------------------------------- abdominal pain
    "abdominal pain": [
        "abdominal pain", "abdominal cramps", "abdominal discomfort",
        "stomach pain", "stomach ache", "stomach cramps",
        "belly pain", "tummy pain", "pain in abdomen",
        "epigastric pain", "lower abdominal pain",
    ],

    # --------------------------------------------------------------- back pain
    "back pain": [
        "back pain", "lower back pain", "upper back pain",
        "backache", "back ache", "spine pain",
        "pain in back", "lumbar pain",
    ],

    # --------------------------------------------------------- swollen glands
    "swollen glands": [
        "swollen glands", "swollen lymph nodes",
        "lymphadenopathy", "enlarged lymph nodes",
        "swollen neck glands", "tender lymph nodes",
    ],

    # ------------------------------------------------------------ sore throat
    "sore throat": [
        "sore throat", "throat pain", "throat ache",
        "painful throat", "difficulty swallowing",
        "throat irritation", "scratchy throat",
        "throat discomfort", "tonsillitis",
    ],

    # -------------------------------------------------------------- runny nose
    "runny nose": [
        "runny nose", "nasal discharge", "nasal drip",
        "postnasal drip", "watery nose", "nose dripping",
    ],

    # --------------------------------------------------------------- congestion
    "congestion": [
        "congestion", "nasal congestion", "stuffy nose",
        "blocked nose", "stuffed up", "nasal blockage",
    ],

    # --------------------------------------------------------------- dizziness
    "dizziness": [
        "dizziness", "dizzy", "lightheadedness",
        "lightheaded", "vertigo", "feeling faint", "faintness",
    ],

    # -------------------------------------------------------- skin discoloration
    "skin discoloration": [
        "yellowing of skin", "yellow skin", "jaundice",
        "yellow eyes", "yellowish skin", "skin yellowing",
        "skin turning yellow",
    ],
}


# ---------------------------------------------------------------------------
# Pre-compile regex patterns (once at module load, not per call)
# ---------------------------------------------------------------------------
# Sorted by length descending so longer phrases ("high fever") match before
# shorter ones ("fever"), preventing partial shadowing.
_COMPILED_PATTERNS: List[Tuple[re.Pattern, str]] = []

for _canonical, _aliases in SYMPTOM_SYNONYMS.items():
    _sorted_aliases = sorted(_aliases, key=len, reverse=True)
    _pattern = re.compile(
        r"\b(" + "|".join(re.escape(a) for a in _sorted_aliases) + r")\b",
        re.IGNORECASE
    )
    _COMPILED_PATTERNS.append((_pattern, _canonical))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def extract_symptoms(text: str) -> List[str]:
    """
    Extract canonical symptom names from a free-text patient description.

    Uses a centralized synonym knowledge base with pre-compiled regex patterns.
    Each matched alias maps to its canonical symptom name.
    Duplicate canonical names are deduplicated.

    Args:
        text: Raw patient symptom description.

    Returns:
        Ordered list of unique canonical symptom names found in the text.
    """
    def normalize_symptom_text(t: str) -> str:
        t = t.lower()
        replacements = {
            r"\bhurts\b": "pain",
            r"\bhurt\b": "pain",
            r"\baching\b": "ache",
            r"\baches\b": "ache",
            r"\bthrow up\b": "vomit",
            r"\bthrowing up\b": "vomiting",
            r"\bpuking\b": "vomiting",
            r"\bpuke\b": "vomit",
            r"\bqueasy\b": "nauseous",
            r"\bspinning\b": "dizzy",
            r"\bpain in my chest\b": "pain in chest",
            r"\bpain in the chest\b": "pain in chest",
        }
        for pat, repl in replacements.items():
            t = re.sub(pat, repl, t)
        return t

    found: List[str] = []
    seen: Set[str] = set()

    normalized_text = normalize_symptom_text(text)

    for pattern, canonical in _COMPILED_PATTERNS:
        if pattern.search(normalized_text) and canonical not in seen:
            found.append(canonical)
            seen.add(canonical)

    return found