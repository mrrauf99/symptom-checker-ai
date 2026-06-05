from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = BASE_DIR / "models" / "disease_model.pkl"

model = joblib.load(MODEL_PATH)


def predict_disease(text: str):

    prediction = model.predict([text])[0]

    probabilities = model.predict_proba([text])[0]

    classes = model.classes_

    results = []

    for disease, score in zip(classes, probabilities):
        results.append({
            "disease": disease,
            "confidence": round(float(score * 100), 2)
        })

    results.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return {
        "prediction": prediction,
        "top_predictions": results[:3]
    }