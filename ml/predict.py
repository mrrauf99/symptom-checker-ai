"""Loads the trained pipeline and performs manual testing in terminal."""
from pathlib import Path
import re

import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "disease_model.pkl"

model = joblib.load(MODEL_PATH)


def _preprocess(text: str) -> str:
    """Normalise hyphens → spaces (mirrors train.py preprocessor)."""
    return re.sub(r"\s+", " ", text.replace("-", " ")).strip()


while True:
    symptom = input("\nDescribe symptoms (or type exit): ")

    if symptom.lower() == "exit":
        break

    prediction = model.predict([symptom])[0]
    probabilities = model.predict_proba([symptom])[0]
    classes = model.classes_

    results = sorted(zip(classes, probabilities), key=lambda x: x[1], reverse=True)

    print(f"\nTop Predictions:")
    for disease, score in results[:5]:
        bar = "█" * int(score * 40)
        print(f"  {disease:<35} {score * 100:5.1f}%  {bar}")