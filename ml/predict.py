import joblib

model = joblib.load("models/disease_model.pkl")

while True:
    symptom = input("\nDescribe symptoms (or type exit): ")

    if symptom.lower() == "exit":
        break

    prediction = model.predict([symptom])[0]

    probabilities = model.predict_proba([symptom])[0]

    classes = model.classes_

    results = list(zip(classes, probabilities))
    results.sort(key=lambda x: x[1], reverse=True)

    print("\nTop Predictions:")

    for disease, score in results[:3]:
        print(f"{disease}: {score * 100:.2f}%")