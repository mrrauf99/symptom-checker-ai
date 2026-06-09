"""Purpose:

Compare predictions

Example:

Pneumonia Case

Check:

Base Model
vs
Boosted Model

Output:

Base:
Pneumonia 61%

Boosted:
Pneumonia 91%

Used for verification."""

import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.services.predictor import predict_disease, _model

_problem_cases = {
    "CASE 1 — Pneumonia": (
        "Persistent cough producing mucus. Chest pain when breathing. "
        "Fever. Chills. Difficulty breathing. Extreme tiredness."
    ),
    "CASE 2 — Chicken Pox": (
        "Mild fever. Fatigue. Rash. Fluid-filled blisters. Itching."
    ),
    "CASE 3 — Bronchial Asthma": (
        "Wheezing. Chest tightness. Shortness of breath. Dry cough."
    ),
    "CASE 4 — Malaria": (
        "Fever. Chills. Sweating. Headache. Weakness. Vomiting. Body aches."
    ),
    "Pneumonia (extended)": (
        "I have a persistent cough that produces greenish mucus. "
        "I have chest pain, high fever, chills, and difficulty breathing. "
        "My chest feels congested."
    ),
    "Chicken Pox (extended)": (
        "I have a fever, an itchy rash all over my body, and fluid-filled blisters "
        "that are spreading. I also feel fatigued."
    ),
    "Dengue (with eye pain)": (
        "I have a sudden high fever with severe headache and pain behind the eyes. "
        "I also have joint pain, muscle pain, and a skin rash on my body."
    ),
    "Malaria (extended)": (
        "Recurring high fever followed by chills and excessive sweating. "
        "Feel extremely weak. Headaches, muscle pain, occasional vomiting."
    ),
    "Arthritis (stiff joints)": (
        "Joint pain in fingers, wrists, and knees. Joints are stiff and swollen, "
        "especially in the morning. I feel fatigued. Pain worsens with movement."
    ),
    "Typhoid": (
        "I have been experiencing sustained high fever for over a week. "
        "I feel very weak and have stomach pain and loss of appetite. "
        "I also have diarrhea and feel exhausted."
    ),
    "Psoriasis": (
        "I have red, itchy scaly patches on my arms, legs, and scalp. "
        "My skin is peeling and the rash keeps spreading to new areas."
    ),
    "Fungal infection": (
        "I have red, itchy patches on my skin with a defined border. "
        "The skin is peeling and the patches are spreading."
    ),
}

print("=" * 60)
print("VERIFICATION — Problematic Cases")
print("=" * 60)
for label, text in _problem_cases.items():
    # Base
    proba = _model.predict_proba([text])[0]
    classes = _model.classes_
    top3_base = sorted(zip(classes, proba), key=lambda x: x[1], reverse=True)[:3]
    top_str_base = "  |  ".join(f"{d}: {s*100:.1f}%" for d, s in top3_base)
    
    # Boosted
    boost_res = predict_disease(text)
    top3_boost = [(x['disease'], x['confidence']/100) for x in boost_res['top_predictions']]
    top_str_boost = "  |  ".join(f"{d}: {s*100:.1f}%" for d, s in top3_boost)
    symptoms = boost_res['symptoms']
    
    print(f"[{label}]")
    print(f"  Base   : {top_str_base}")
    print(f"  Boosted: {top_str_boost}")
    print(f"  Symptoms: {symptoms}\n")
