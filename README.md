# Symptom Checker AI

A full-stack healthcare assistant that predicts likely diseases from free-text symptom descriptions. The project combines a Python FastAPI backend, a React/Vite frontend, and a scikit-learn based machine learning model with clinical symptom boosting.

## Key Features

- Predicts disease based on symptom descriptions
- Provides confidence scores and human-readable confidence levels
- Extracts canonical symptom terms from user input
- Recommends a medical specialist for each predicted condition
- Supports user authentication, profile management, session history, and chat interaction
- Includes an interactive frontend dashboard and chat interface

## Repository Structure

- `backend/` — FastAPI backend services, routes, authentication, and prediction logic
- `frontend/` — React/Vite web application for the user interface
- `ml/` — Model training, prediction CLI, and evaluation scripts
- `models/` — Serialized trained model artifact
- `text_preprocessor.py` — Shared text normalization utilities used by training and prediction
- `requirements.txt` — Python backend dependencies

## Architecture

### Backend

- `backend/main.py` — FastAPI application entrypoint
- `backend/routes/` — API routes for auth, chat, profile, session, and prediction
- `backend/services/predictor.py` — Disease prediction service with ML and symptom boosting
- `backend/services/symptom_extractor.py` — Canonical symptom extraction from natural language

### Machine Learning

- `ml/train.py` — Trains the disease classifier and stores the best model to `models/disease_model.pkl`
- `ml/predict.py` — CLI for interactive symptom prediction
- `ml/evaluate_boosting.py` — Compares raw ML output with boosted prediction results
- `ml/data/Symptom2Disease.csv` — Training dataset containing symptom descriptions labeled by disease

### Frontend

- `frontend/package.json` — React/Vite app dependencies and scripts
- `frontend/src/` — Application source code, including pages, layout, API clients, and UI components
- `frontend/src/App.jsx` — Route definitions and protected route handling
- `frontend/src/main.jsx` — App bootstrap with router and auth provider

## Installation

### Backend Setup

1. Create a Python virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

3. Install backend dependencies:

```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Install frontend dependencies:

```bash
cd frontend
npm install
```

## Running the Application

### Start the Backend

From the project root:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Start the Frontend

From the `frontend/` folder:

```bash
npm run dev
```

The frontend should open at `http://localhost:5173` and communicate with the backend at `http://localhost:8000`.

## Model Workflow

1. User submits symptom text
2. Text is normalized by `text_preprocessor.py`
3. Symptoms are extracted using `backend/services/symptom_extractor.py`
4. The trained sklearn pipeline predicts disease probabilities
5. Symptom-based boosting adjusts probabilities using clinical rules
6. Final prediction and metadata are returned to the frontend

## Prediction Response Format

The backend returns a JSON object with:

- `prediction` — top predicted disease
- `confidence` — numeric confidence percentage
- `confidence_level` — `High`, `Medium`, or `Low`
- `top_predictions` — top three disease predictions with confidence values
- `symptoms` — extracted canonical symptom names
- `specialist` — recommended medical specialist

## Training and Evaluation

### Retrain the Model

Run the training script to rebuild the pipeline and model artifact:

```bash
python ml/train.py
```

### Evaluate Boosting

Validate the symptom-based boosting logic with examples:

```bash
python ml/evaluate_boosting.py
```

## Notes

- The frontend app is implemented with React, React Router, Tailwind CSS, and Axios
- The backend API uses FastAPI and includes CORS support for local frontend development
- The model artifact is serialized with `joblib` and loaded once at startup
- The symptom extraction and boosting layers are designed to preserve ML output while improving clinical relevance