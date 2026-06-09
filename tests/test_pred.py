import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from backend.services.symptom_extractor import extract_symptoms
from backend.services.predictor import _model, _apply_symptom_boost, predict_disease

text = "I have a persistent cough producing mucus. I experience chest pain whenever I take a deep breath. I have a fever, chills, difficulty breathing, and extreme tiredness."
symptoms = extract_symptoms(text)
raw_probabilities = _model.predict_proba([text])[0]
classes = _model.classes_

asthma_idx = np.where(classes == "Bronchial Asthma")[0][0]
pneumonia_idx = np.where(classes == "Pneumonia")[0][0]

print("Raw Asthma:", raw_probabilities[asthma_idx])
print("Raw Pneumonia:", raw_probabilities[pneumonia_idx])

print("Final Prediction:", predict_disease(text)["prediction"])
