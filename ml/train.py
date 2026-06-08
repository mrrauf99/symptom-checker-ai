"""
ML Training Pipeline — v3
=========================
Changes from v2:
  - TF-IDF: trigrams (1,3), max_features=15000, min_df=1 (was 2),
    captures terse clinical phrases better
  - Classifier: class_weight='balanced' on LogisticRegression
  - Text preprocessor v2: phrase preservation, lowercasing, punctuation removal
  - Model comparison: added balanced variants for LogReg and LinearSVC

Changes from v1:
  - Added _preprocess() text normaliser
  - TF-IDF: bigrams (1,2), sublinear_tf=True, max_features=10000, min_df=2
  - Classifier: CalibratedClassifierCV wrapping LogisticRegression(C=5.0)
  - Reports: accuracy, macro F1, full classification_report
"""

from pathlib import Path

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline, FunctionTransformer
from sklearn.metrics import accuracy_score, f1_score, classification_report

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "disease_model.pkl"


# ---------------------------------------------------------------------------
# Make sure the project root is on the path so that text_preprocessor can be
# imported regardless of how this script is invoked (python ml/train.py).
# ---------------------------------------------------------------------------
import sys
BASE_DIR_STR = str(Path(__file__).resolve().parent.parent)
if BASE_DIR_STR not in sys.path:
    sys.path.insert(0, BASE_DIR_STR)

from text_preprocessor import preprocess_text


# ---------------------------------------------------------------------------
# Load dataset
# ---------------------------------------------------------------------------
df = pd.read_csv(BASE_DIR / "ml" / "data" / "Symptom2Disease.csv")

X = df["text"]
y = df["label"]

print(f"Dataset: {len(df)} rows, {y.nunique()} classes")
print(f"Class distribution:\n{y.value_counts().to_string()}\n")

# ---------------------------------------------------------------------------
# Train / test split — stratified to maintain class balance
# ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------------------------------------------------------------------------
# TF-IDF configuration (shared across model comparison)
# ---------------------------------------------------------------------------
_tfidf_config = dict(
    ngram_range=(1, 3),
    max_features=15_000,
    sublinear_tf=True,
    min_df=1,
    strip_accents="unicode",
    stop_words="english",
)

# ---------------------------------------------------------------------------
# Model Comparison
# ---------------------------------------------------------------------------
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

_comparison_models = {
    "LogReg-C5-balanced": Pipeline([
        ("pre",  FunctionTransformer(preprocess_text)),
        ("tfidf", TfidfVectorizer(**_tfidf_config)),
        ("clf",  CalibratedClassifierCV(
            LogisticRegression(
                C=5.0, max_iter=2000, solver="lbfgs",
                class_weight="balanced", random_state=42
            ),
            cv=5, method="isotonic"
        )),
    ]),
    "LogReg-C5-unbalanced": Pipeline([
        ("pre",  FunctionTransformer(preprocess_text)),
        ("tfidf", TfidfVectorizer(**_tfidf_config)),
        ("clf",  CalibratedClassifierCV(
            LogisticRegression(C=5.0, max_iter=2000, solver="lbfgs", random_state=42),
            cv=5, method="isotonic"
        )),
    ]),
    "LinearSVC-Cal-balanced": Pipeline([
        ("pre",  FunctionTransformer(preprocess_text)),
        ("tfidf", TfidfVectorizer(**_tfidf_config)),
        ("clf",  CalibratedClassifierCV(
            LinearSVC(C=1.0, max_iter=2000, class_weight="balanced", random_state=42),
            cv=5, method="isotonic"
        )),
    ]),
    "MultinomialNB": Pipeline([
        ("pre",  FunctionTransformer(preprocess_text)),
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 3), max_features=15_000, min_df=1, stop_words="english"
        )),
        ("clf",  MultinomialNB()),
    ]),
    "RandomForest-200": Pipeline([
        ("pre",  FunctionTransformer(preprocess_text)),
        ("tfidf", TfidfVectorizer(**_tfidf_config)),
        ("clf",  RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42, n_jobs=-1)),
    ]),
}

print(f"{'Model':<25} {'Accuracy':>9} {'F1 Macro':>9}")
print("-" * 45)
for name, m in _comparison_models.items():
    m.fit(X_train, y_train)
    preds = m.predict(X_test)
    acc = accuracy_score(y_test, preds)
    f1  = f1_score(y_test, preds, average="macro")
    print(f"{name:<25} {acc:>9.4f} {f1:>9.4f}")

print()

# ---------------------------------------------------------------------------
# Primary model — LinearSVC with isotonic calibration
# (selected from comparison: 97.08% accuracy, best F1 on this TF-IDF config.
#  CalibratedClassifierCV provides predict_proba for confidence + boosting.)
# ---------------------------------------------------------------------------
model = Pipeline([
    ("pre",  FunctionTransformer(preprocess_text)),
    ("tfidf", TfidfVectorizer(**_tfidf_config)),
    ("clf",  CalibratedClassifierCV(
        LinearSVC(
            C=1.0,
            max_iter=2000,
            class_weight="balanced",
            random_state=42
        ),
        cv=5,
        method="isotonic"
    )),
])

# ---------------------------------------------------------------------------
# Train
# ---------------------------------------------------------------------------
print("Training selected model (LinearSVC-Cal-balanced with v2 preprocessor)...")
model.fit(X_train, y_train)

# ---------------------------------------------------------------------------
# Evaluate
# ---------------------------------------------------------------------------
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
f1 = f1_score(y_test, predictions, average="macro")

print(f"\nAccuracy : {accuracy:.4f}")
print(f"F1 (macro): {f1:.4f}")
print()
print(classification_report(y_test, predictions))

# ---------------------------------------------------------------------------
# Verify problematic cases
# ---------------------------------------------------------------------------
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
    proba = model.predict_proba([text])[0]
    classes = model.classes_
    top3 = sorted(zip(classes, proba), key=lambda x: x[1], reverse=True)[:3]
    top_str = "  |  ".join(f"{d}: {s*100:.1f}%" for d, s in top3)
    print(f"[{label}]\n  {top_str}\n")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
MODEL_DIR.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")