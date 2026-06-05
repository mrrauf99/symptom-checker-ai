SYMPTOMS = [
    "fever",
    "headache",
    "cough",
    "fatigue",
    "nausea",
    "vomiting",
    "chills",
    "joint pain",
    "skin rash"
]


def extract_symptoms(text: str):

    text = text.lower()

    found = []

    for symptom in SYMPTOMS:
        if symptom in text:
            found.append(symptom)

    return found