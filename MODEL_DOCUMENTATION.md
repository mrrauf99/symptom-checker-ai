# 🏥 Symptom-to-Disease Prediction Model Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Core Model Architecture](#core-model-architecture)
3. [Detailed Component Breakdown](#detailed-component-breakdown)
4. [Complete Prediction Flow](#complete-prediction-flow)
5. [Key Files Explained](#key-files-explained)
6. [Confidence Levels](#confidence-levels)
7. [How It's Used](#how-its-used)

---

## Project Overview

This project is a **disease prediction AI system** that analyzes patient symptom descriptions and recommends likely diagnoses using machine learning combined with clinical boosting logic.

**Key Capabilities:**

- Predicts disease from free-text symptom descriptions
- Provides confidence scores with clinical confidence levels
- Recommends appropriate medical specialists
- Extracts and returns canonical symptom names
- Applies clinical domain knowledge to improve accuracy

---

## Core Model Architecture

### Machine Learning Pipeline

Your model uses a **3-stage sklearn Pipeline**:

| Stage              | Component                                   | Purpose                                       |
| ------------------ | ------------------------------------------- | --------------------------------------------- |
| **Preprocessing**  | `FunctionTransformer` + `preprocess_text()` | Normalizes text before vectorization          |
| **Vectorization**  | `TfidfVectorizer`                           | Converts symptom text into numerical features |
| **Classification** | `LinearSVC + CalibratedClassifierCV`        | Predicts disease class with confidence scores |

### Key Configuration

- **TF-IDF Parameters**:
  - Trigrams (1-3): Captures single words, bigrams, and trigrams
  - max_features: 15,000
  - sublinear_tf: True (reduces impact of high-frequency terms)
  - min_df: 1 (include even rare symptoms)
  - stop_words: English removed

- **Classifier**:
  - LinearSVC (Support Vector Classifier)
  - Wrapped with CalibratedClassifierCV for probability outputs
  - Isotonic calibration method (cv=5)
  - Class weight: balanced (handles class imbalance)

- **Training Data**:
  - `ml/data/Symptom2Disease.csv`
  - Contains text descriptions → disease labels
  - Stratified 80-20 train-test split

- **Performance**:
  - ~97.08% accuracy on test set
  - Best F1 score among tested models

- **Model Storage**:
  - Serialized as `models/disease_model.pkl`
  - Loaded once on backend startup (singleton pattern)

### Model Comparison

During training, 5 models are evaluated. **LinearSVC-Cal-balanced** was selected:

| Model                      | Accuracy   | F1 Score | Selected |
| -------------------------- | ---------- | -------- | -------- |
| LogReg-C5-balanced         | Lower      | Lower    | ❌       |
| LogReg-C5-unbalanced       | Lower      | Lower    | ❌       |
| **LinearSVC-Cal-balanced** | **97.08%** | **Best** | ✅       |
| MultinomialNB              | Lower      | Lower    | ❌       |
| RandomForest-200           | Lower      | Lower    | ❌       |

---

## Detailed Component Breakdown

### 1. Text Preprocessing (`text_preprocessor.py`)

**Purpose**: Normalizes raw symptom text to improve model accuracy

**Process**:

1. **Phrase Preservation Map**: Medical phrases stay together as single tokens

   ```
   "fluid-filled blisters"     → "fluid_filled_blisters"
   "pain behind the eyes"      → "pain_behind_eyes"
   "shortness of breath"       → "shortness_of_breath"
   "chest tightness"           → "chest_tightness"
   "chest congestion"          → "chest_congestion"
   "productive cough"          → "productive_cough"
   ```

2. **Lowercasing**: Convert to lowercase for consistent matching

   ```
   "Fever" → "fever"
   ```

3. **Punctuation Removal**: Strip sentence-ending punctuation

   ```
   "Fever." → "Fever"
   ```

4. **Hyphen Normalization**: Convert hyphens to spaces
   ```
   "fluid-filled" → "fluid filled"
   ```

**Why?** Prevents TF-IDF from splitting clinical phrases into disconnected tokens, preserving semantic meaning and improving feature quality.

---

### 2. Symptom Extraction (`backend/services/symptom_extractor.py`)

**Purpose**: Maps free-text user input to canonical symptom names (single source of truth)

**Canonical Symptoms** (partial list):

```python
"fever": ["high fever", "feverish", "temperature", "pyrexia", ...]
"wheezing": ["wheezing", "wheeze", "whistling breath", ...]
"blisters": ["blisters", "itchy blisters", "skin blisters", "vesicles", ...]
"joint pain": ["joint pain", "joint stiffness", "morning stiffness", ...]
"productive cough": ["productive cough", "mucus cough", "phlegm", ...]
"chest pain": ["chest pain", "chest ache", "thoracic pain", ...]
"chest tightness": ["chest tightness", "chest constriction", ...]
"shortness of breath": ["shortness of breath", "difficulty breathing", ...]
"silvery scales": ["silvery scales", "flaky patches", "scaling skin", ...]
"pain behind eyes": ["pain behind eyes", "pain behind the eyes", ...]
"recurring fever": ["recurring fever", "cyclical fever", "periodic fever", ...]
```

**Key Design Features**:

- Sorted longest-first (multi-word phrases match before shorter ones)
- Compiled once at import time for performance
- Used by boosting rules to identify clinical patterns

---

### 3. ML Prediction (`ml/train.py`)

**Pipeline Assembly**:

```python
model = Pipeline([
    ("pre",   FunctionTransformer(preprocess_text)),
    ("tfidf", TfidfVectorizer(...)),
    ("clf",   CalibratedClassifierCV(
        LinearSVC(...), cv=5, method="isotonic"
    ))
])
```

**Training Steps**:

1. Load CSV dataset with symptom text and disease labels
2. Stratified train-test split (80-20, maintaining class distribution)
3. Fit TF-IDF vectorizer on training data
4. Train LinearSVC classifier
5. Calibrate with isotonic calibration (5-fold CV)
6. Evaluate on test set (accuracy, F1 macro, classification report)
7. Serialize to `models/disease_model.pkl`

**Output**: Raw probability distribution over all disease classes

```python
# Example
classes = ["Pneumonia", "Asthma", "Malaria", "Dengue", ...]
probabilities = [0.45, 0.25, 0.15, 0.10, ...]
```

---

### 4. Symptom-Based Boosting Layer (`backend/services/predictor.py`)

**Problem Addressed**:

- Raw ML predictions aren't always clinically intuitive
- User input is often terse ("I have chills and sweating")
- Model was trained on detailed descriptions
- Need to bridge gap between sparse user input and training distribution

**Solution**: Rule-based boosting layer that applies clinical domain knowledge

**Boost Rules** (examples):

#### Malaria Rule

```python
{
    "disease": "Malaria",
    "required": {"chills", "sweating"},      # MUST have both
    "partial": {"fever", "headache", "vomiting", "muscle pain"},
    "partial_threshold": 2,                  # Need ≥2 of these
    "boost": 0.22,                           # Add 22% if full match
    "partial_boost": 0.10,                   # Add 10% if partial match
    "dampen": {"Typhoid": 0.20}              # Reduce Typhoid by 20%
}
```

#### Pneumonia Rule

```python
{
    "disease": "Pneumonia",
    "required": {"productive cough"},
    "partial": {"chest pain", "fever", "chest congestion", "chills", "shortness of breath"},
    "partial_threshold": 2,
    "boost": 0.30,
    "partial_boost": 0.12,
    "dampen": {"Bronchial Asthma": 0.65}     # Asthma = dry cough, not productive
}
```

#### Bronchial Asthma Rule

```python
{
    "disease": "Bronchial Asthma",
    "required": {"wheezing"},
    "partial": {"chest tightness", "shortness of breath", "cough"},
    "partial_threshold": 2,
    "boost": 0.25,
    "partial_boost": 0.12,
    "dampen": {}
}
```

**Complete Boost Rules Include**:

- Bronchial Asthma (wheezing → high weight)
- Pneumonia (productive cough → high weight)
- Chicken Pox (blisters → high weight, dampens Impetigo)
- Malaria (chills + sweating → high weight, dampens Typhoid)
- Dengue (pain behind eyes → unique indicator)
- Typhoid (loss of appetite → GI-dominant)
- Arthritis (joint pain → high weight, dampens Psoriasis)
- Psoriasis (silvery scales → distinctive)

**Algorithm**:

1. Check each rule's required and partial symptoms against extracted symptoms
2. If **full match** (all required + enough partial):
   - Add `boost` probability mass to disease
   - Apply dampening to confused diseases
3. If **partial match** (required OR enough partial):
   - Add `partial_boost` probability mass
   - Apply half dampening
4. Ensure no negative values
5. **Re-normalize** so probabilities sum to 1.0

**Why This Works**:

- Lightweight ranking adjustment (not hardcoded override)
- Respects ML model's learned patterns
- Applies clinical domain knowledge
- Backward compatible with existing API

---

### 5. Disease Prediction Service (`backend/services/predictor.py`)

**Public API**: `predict_disease(text: str) → Dict[str, Any]`

**Pipeline**:

1. Load model (if not already loaded)
2. Extract canonical symptoms from input text
3. Get raw ML probabilities
4. Apply symptom-based boosting
5. Format response with metadata

**Response Structure**:

```python
{
    "prediction": "Malaria",                    # Top predicted disease
    "confidence": 67.5,                         # Confidence % (0-100)
    "confidence_level": "High",                 # "High" | "Medium" | "Low"
    "top_predictions": [                        # Top-3 with details
        {
            "disease": "Malaria",
            "confidence": 67.5,
            "confidence_level": "High"
        },
        {
            "disease": "Typhoid",
            "confidence": 24.3,
            "confidence_level": "Medium"
        },
        {
            "disease": "Dengue",
            "confidence": 8.2,
            "confidence_level": "Low"
        }
    ],
    "symptoms": ["fever", "chills", "sweating", "muscle pain"],  # Extracted symptoms
    "specialist": "Infectious Disease Specialist"                 # Recommended specialist
}
```

---

## Complete Prediction Flow

### End-to-End Example

**Input**:

```
"I have fever, chills, sweating, and muscle pain"
```

**Step 1: Text Preprocessing**

```
Raw:       "I have fever, chills, sweating, and muscle pain"
Processed: "i have fever chills sweating and muscle pain"
           (lowercased, punctuation removed)
```

**Step 2: Symptom Extraction**

```
Extracted Symptoms: ["fever", "chills", "sweating", "muscle pain"]
```

**Step 3: ML Prediction**

```
TF-IDF Vectorization:
  → Convert text to numerical features based on word/phrase frequencies

LinearSVC + Calibration:
  → Predict class probabilities

Raw Output (before boosting):
  Malaria: 0.45
  Typhoid: 0.30
  Dengue: 0.15
  Pneumonia: 0.05
  Asthma: 0.03
  [+ others...]
```

**Step 4: Symptom-Based Boosting**

```
Detected symptoms set: {"fever", "chills", "sweating", "muscle pain"}

Apply Malaria rule:
  - Required: {"chills", "sweating"} ✓ Both present
  - Partial: {"fever", "headache", "vomiting", "muscle pain"}
  - Partial matches: fever ✓, muscle pain ✓ (2 out of 4)
  - Full match! (required ✓ + partial_matches ≥ threshold)
  - Add boost: +0.22
  - Apply dampen: Typhoid *= (1 - 0.20) = 0.24

  Malaria: 0.45 + 0.22 = 0.67
  Typhoid: 0.30 * 0.80 = 0.24

Normalize (sum = 1.0):
  Malaria: 0.67 / 1.19 ≈ 0.563
  Typhoid: 0.24 / 1.19 ≈ 0.202
  [others rescaled...]
```

**Step 5: Format Response**

```json
{
  "prediction": "Malaria",
  "confidence": 56.3,
  "confidence_level": "Medium",
  "top_predictions": [
    { "disease": "Malaria", "confidence": 56.3, "confidence_level": "Medium" },
    { "disease": "Typhoid", "confidence": 20.2, "confidence_level": "Low" },
    { "disease": "Dengue", "confidence": 12.6, "confidence_level": "Low" }
  ],
  "symptoms": ["fever", "chills", "sweating", "muscle pain"],
  "specialist": "Infectious Disease Specialist"
}
```

---

## Key Files Explained

### Machine Learning & Model Training

| File                              | Purpose                                                                                                                                            |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`ml/train.py`**                 | Main training script. Tests 5 models, selects LinearSVC, saves to `models/disease_model.pkl`. Implements TF-IDF with trigrams and class balancing. |
| **`ml/predict.py`**               | Interactive CLI for testing predictions. Load model and loop for user input.                                                                       |
| **`ml/evaluate_boosting.py`**     | Validates boosting layer on 12 test cases comparing base ML vs boosted predictions.                                                                |
| **`ml/data/Symptom2Disease.csv`** | Training dataset with columns: `label` (disease), `text` (symptom description). Multiple examples per disease.                                     |
| **`models/disease_model.pkl`**    | Serialized trained sklearn Pipeline. Loaded at backend startup.                                                                                    |

### Backend Services

| File                                        | Purpose                                                                                                                |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **`backend/services/predictor.py`**         | Production prediction API. Loads model, applies boosting, returns response. Entry point: `predict_disease(text)`.      |
| **`backend/services/symptom_extractor.py`** | Extracts canonical symptoms from text. Central symptom knowledge base (SYMPTOM_SYNONYMS).                              |
| **`text_preprocessor.py`**                  | Shared text normalization. Phrase preservation, lowercasing, punctuation removal. Used by both train.py and model.pkl. |

### API Integration

| File                                | Purpose                                                                   |
| ----------------------------------- | ------------------------------------------------------------------------- |
| **`backend/routes/chat_routes.py`** | Exposes prediction via REST API. POST `/chat/predict` endpoint.           |
| **`frontend/src/api/chatAPI.js`**   | JavaScript client for prediction. Calls backend `/chat/predict` endpoint. |

### Testing & Evaluation

| File                                  | Purpose                             |
| ------------------------------------- | ----------------------------------- |
| **`tests/test_predictor.py`**         | Unit tests for prediction service.  |
| **`tests/test_symptom_extractor.py`** | Unit tests for symptom extraction.  |
| **`tests/test_confidence.py`**        | Tests confidence level calculation. |

---

## Confidence Levels

Numeric confidence scores are mapped to human-readable levels:

| Confidence Range  | Level      | Interpretation           | Action                                     |
| ----------------- | ---------- | ------------------------ | ------------------------------------------ |
| **≥ 70%**         | **High**   | Strong clinical evidence | Take seriously, see specialist immediately |
| **≥ 40% & < 70%** | **Medium** | Moderate confidence      | Consider diagnosis, monitor symptoms       |
| **< 40%**         | **Low**    | Weak evidence            | Inconclusive, need more information        |

**Example**:

- Malaria at 67.5% → "Medium" (high number, but below 70% threshold)
- Pneumonia at 85% → "High"
- Psoriasis at 35% → "Low"

---

## How It's Used

### Backend REST API

**Endpoint**: `POST /chat/predict`

**Request**:

```json
{
  "text": "I have persistent cough and chest pain with difficulty breathing"
}
```

**Response**:

```json
{
  "prediction": "Pneumonia",
  "confidence": 78.5,
  "confidence_level": "High",
  "top_predictions": [
    {
      "disease": "Pneumonia",
      "confidence": 78.5,
      "confidence_level": "High"
    },
    {
      "disease": "Bronchial Asthma",
      "confidence": 15.3,
      "confidence_level": "Low"
    },
    {
      "disease": "Tuberculosis",
      "confidence": 6.2,
      "confidence_level": "Low"
    }
  ],
  "symptoms": ["productive cough", "chest pain", "shortness of breath"],
  "specialist": "Pulmonologist"
}
```

### Frontend Integration

The React frontend (`frontend/src/components/prediction/`) displays:

- **Prediction**: Top disease name with confidence percentage
- **Confidence Breakdown**: Visual bar chart of top-3 predictions
- **Symptoms Section**: List of extracted canonical symptoms
- **Health Advice**: Specialist recommendation and medical disclaimer
- **Analyzing Message**: Loading state during prediction

---

## Model Lifecycle

### Training (Offline)

```
1. Load ml/data/Symptom2Disease.csv
2. Split data (80% train, 20% test, stratified)
3. Compare 5 models
4. Select LinearSVC-Cal-balanced
5. Save to models/disease_model.pkl
```

### Production (Online)

```
1. Backend startup: Load models/disease_model.pkl (singleton)
2. User input received at /chat/predict
3. Run prediction pipeline:
   - Preprocess text
   - Extract symptoms
   - Get ML probabilities
   - Apply symptom boosting
4. Return JSON response
5. Frontend displays results
```

---

## Version History

### Train.py Evolution

- **v1**: Initial TF-IDF (bigrams), LogisticRegression, basic preprocessing
- **v2**: Added phrase preservation, sublinear TF-IDF, CalibratedClassifierCV
- **v3**: Trigrams (1,3), max_features=15000, min_df=1, class_weight='balanced'

### Predictor.py Evolution

- **v1**: Basic ML prediction only
- **v2**: Added symptom extraction and specialist recommendation
- **v3**: Added symptom-based boosting layer for improved accuracy

### Symptom Extractor Evolution

- **v1**: Basic canonical symptoms
- **v2**: Added pain behind eyes, blisters, chest congestion, silvery scales
- **v3**: Split wheezing, chest tightness, added productive cough, recurring fever

---

## Technical Stack

- **ML Framework**: scikit-learn
- **Vectorization**: TF-IDF (sklearn)
- **Classifier**: LinearSVC + Isotonic Calibration
- **Model Serialization**: joblib
- **Backend**: FastAPI/Python
- **Frontend**: React
- **Database**: MongoDB (for storing prediction history)

---

## Notes & Best Practices

1. **Model Loading**: The model is loaded once at backend startup (singleton pattern) for performance
2. **Preprocessing Consistency**: Both training and prediction use the same `preprocess_text()` function
3. **Backward Compatibility**: New fields (symptoms, specialist, boosting) are additive; all existing API contracts preserved
4. **Boosting Philosophy**: Lightweight ranking adjustment, respects ML learning, applies clinical domain knowledge
5. **Confidence Thresholds**: Calibrated empirically; can be adjusted per deployment requirements

---

## Extending the Model

### Add a New Symptom

1. Add to `SYMPTOM_SYNONYMS` in `backend/services/symptom_extractor.py`
2. Retrain model if symptom is new to training data

### Add a Boosting Rule

1. Add rule dict to `_BOOST_RULES` in `backend/services/predictor.py`
2. Define required/partial symptoms, boost/partial_boost amounts, dampening

### Retrain the Model

```bash
python ml/train.py
```

This will:

- Load fresh CSV data
- Compare 5 algorithms
- Train LinearSVC
- Save to `models/disease_model.pkl`

### Evaluate Boosting

```bash
python ml/evaluate_boosting.py
```

This will compare base ML predictions vs boosted predictions on test cases.

---

**Last Updated**: 2026-06-08  
**Model Version**: v3  
**Accuracy**: 97.08%
