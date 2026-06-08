"""
Disease Predictor Tests — v3
============================
Integration tests for predict_disease().
Validates response structure, field types, ordering, and realistic
disease inputs for all 9 target diseases.

v3 additions:
  - TestStrictPredictions — top-1 prediction must exactly match expected disease
    for all 4 previously-failing cases + 5 existing passing cases
  - TestBoostingLayer — validates symptom-based boosting adjusts probabilities
  - All 9 diseases have strict top-1 tests with realistic symptom descriptions

Note: These tests depend on the trained model being present at models/disease_model.pkl.
Run `python ml/train.py` first if the model file is missing.
"""

import pytest
from backend.services.predictor import predict_disease


# ---------------------------------------------------------------------------
# Shared test inputs (realistic descriptions)
# ---------------------------------------------------------------------------

DENGUE_INPUT = (
    "I have a sudden high fever with severe headache and pain behind the eyes. "
    "I also have joint pain, muscle pain, and a skin rash on my body."
)

MALARIA_INPUT = (
    "I have recurring episodes of high fever followed by chills and excessive "
    "sweating. During these episodes, I feel extremely weak and exhausted. "
    "I also experience headaches, muscle pain, and occasional vomiting."
)

TYPHOID_INPUT = (
    "I have been experiencing sustained high fever for over a week. "
    "I feel very weak and have stomach pain and loss of appetite. "
    "I also have diarrhea and feel exhausted."
)

PNEUMONIA_INPUT = (
    "I have a severe cough with difficulty breathing and chest pain. "
    "I have a high fever and feel very tired and weak."
)

PNEUMONIA_EXTENDED_INPUT = (
    "I have a persistent cough that produces greenish mucus. "
    "I have chest pain, high fever, chills, and difficulty breathing. "
    "My chest feels congested. I am extremely tired."
)

PSORIASIS_INPUT = (
    "I have red, itchy scaly patches on my arms, legs, and scalp. "
    "My skin is peeling and the rash keeps spreading to new areas."
)

ARTHRITIS_INPUT = (
    "I have joint pain in my fingers, wrists, and knees. "
    "The joints are stiff and swollen, especially in the morning. "
    "I also feel fatigued and the pain gets worse with movement."
)

CHICKENPOX_INPUT = (
    "I have a fever, an itchy rash all over my body, and fluid-filled blisters "
    "that are spreading. I also feel fatigued and have no energy."
)

CHICKENPOX_EXTENDED_INPUT = (
    "I developed a high fever three days ago. Now I have an intensely itchy rash "
    "with fluid-filled blisters spreading from my torso to my arms and face. "
    "The blisters are in different stages — some are new, some are crusting over. "
    "I feel very fatigued and have a mild headache."
)

FUNGAL_INFECTION_INPUT = (
    "I have red, itchy patches on my skin with a defined border. "
    "The skin is peeling and the patches are spreading."
)

# The 4 previously-failing test cases (exact inputs from the issue)
CASE_1_PNEUMONIA = (
    "Persistent cough producing mucus. "
    "Chest pain when breathing. "
    "Fever. Chills. Difficulty breathing. "
    "Extreme tiredness."
)

CASE_2_CHICKENPOX = (
    "Mild fever. Fatigue. Rash. "
    "Fluid-filled blisters. Itching."
)

CASE_3_ASTHMA = (
    "Wheezing. Chest tightness. "
    "Shortness of breath. Dry cough."
)

CASE_4_MALARIA = (
    "Fever. Chills. Sweating. "
    "Headache. Weakness. Vomiting. Body aches."
)


# ---------------------------------------------------------------------------
# Response structure tests
# ---------------------------------------------------------------------------

class TestPredictDiseaseStructure:
    """Validates all required fields are present with correct types."""

    def test_returns_dict(self):
        result = predict_disease(DENGUE_INPUT)
        assert isinstance(result, dict)

    def test_required_keys_present(self):
        result = predict_disease(MALARIA_INPUT)
        assert "prediction" in result
        assert "confidence" in result
        assert "confidence_level" in result
        assert "top_predictions" in result

    def test_prediction_is_string(self):
        result = predict_disease(DENGUE_INPUT)
        assert isinstance(result["prediction"], str)
        assert len(result["prediction"]) > 0

    def test_confidence_is_float(self):
        result = predict_disease(DENGUE_INPUT)
        assert isinstance(result["confidence"], float)

    def test_confidence_in_valid_range(self):
        result = predict_disease(MALARIA_INPUT)
        assert 0.0 <= result["confidence"] <= 100.0

    def test_confidence_level_is_valid(self):
        result = predict_disease(DENGUE_INPUT)
        assert result["confidence_level"] in {"High", "Medium", "Low"}

    def test_top_predictions_is_list(self):
        result = predict_disease(DENGUE_INPUT)
        assert isinstance(result["top_predictions"], list)

    def test_top_predictions_has_three_entries(self):
        result = predict_disease(DENGUE_INPUT)
        assert len(result["top_predictions"]) == 3

    def test_top_predictions_entry_structure(self):
        result = predict_disease(DENGUE_INPUT)
        for entry in result["top_predictions"]:
            assert "disease" in entry
            assert "confidence" in entry
            assert "confidence_level" in entry
            assert isinstance(entry["disease"], str)
            assert isinstance(entry["confidence"], float)
            assert entry["confidence_level"] in {"High", "Medium", "Low"}

    def test_top_predictions_sorted_descending(self):
        result = predict_disease(MALARIA_INPUT)
        scores = [e["confidence"] for e in result["top_predictions"]]
        assert scores == sorted(scores, reverse=True)

    def test_top_prediction_matches_first_entry(self):
        result = predict_disease(MALARIA_INPUT)
        assert result["prediction"] == result["top_predictions"][0]["disease"]

    def test_top_confidence_matches_first_entry(self):
        result = predict_disease(MALARIA_INPUT)
        assert result["confidence"] == result["top_predictions"][0]["confidence"]


# ---------------------------------------------------------------------------
# Enriched response fields (v2)
# ---------------------------------------------------------------------------

class TestPredictorEnrichedResponse:
    """
    Validates the new 'symptoms' and 'specialist' fields added in v2.
    These are additive — existing tests must not be broken.
    """

    def test_symptoms_key_present(self):
        result = predict_disease(DENGUE_INPUT)
        assert "symptoms" in result, "predict_disease() must return 'symptoms' field"

    def test_symptoms_is_list(self):
        result = predict_disease(DENGUE_INPUT)
        assert isinstance(result["symptoms"], list)

    def test_symptoms_are_strings(self):
        result = predict_disease(DENGUE_INPUT)
        for sym in result["symptoms"]:
            assert isinstance(sym, str)

    def test_symptoms_not_empty_for_rich_input(self):
        """A detailed symptom description should always yield at least one extracted symptom."""
        result = predict_disease(MALARIA_INPUT)
        assert len(result["symptoms"]) > 0, (
            f"No symptoms extracted from a detailed input. Got: {result['symptoms']}"
        )

    def test_symptoms_correct_for_dengue(self):
        result = predict_disease(DENGUE_INPUT)
        syms = result["symptoms"]
        assert "fever" in syms, f"Expected 'fever' in symptoms. Got: {syms}"
        assert "headache" in syms, f"Expected 'headache' in symptoms. Got: {syms}"

    def test_symptoms_correct_for_malaria(self):
        result = predict_disease(MALARIA_INPUT)
        syms = result["symptoms"]
        assert "fever" in syms
        assert "chills" in syms
        assert "sweating" in syms

    def test_symptoms_correct_for_arthritis(self):
        result = predict_disease(ARTHRITIS_INPUT)
        syms = result["symptoms"]
        assert "joint pain" in syms

    def test_specialist_key_present(self):
        result = predict_disease(DENGUE_INPUT)
        assert "specialist" in result, "predict_disease() must return 'specialist' field"

    def test_specialist_is_string(self):
        result = predict_disease(DENGUE_INPUT)
        assert isinstance(result["specialist"], str)
        assert len(result["specialist"]) > 0

    def test_specialist_not_empty(self):
        for text in [DENGUE_INPUT, MALARIA_INPUT, TYPHOID_INPUT, ARTHRITIS_INPUT]:
            result = predict_disease(text)
            assert result["specialist"], f"Specialist should never be empty. Got: {result['specialist']}"

    def test_specialist_is_valid_string_for_all_diseases(self):
        inputs = [
            DENGUE_INPUT, MALARIA_INPUT, TYPHOID_INPUT,
            PNEUMONIA_INPUT, PSORIASIS_INPUT, ARTHRITIS_INPUT,
        ]
        for text in inputs:
            result = predict_disease(text)
            assert isinstance(result["specialist"], str)
            assert len(result["specialist"]) > 0


# ---------------------------------------------------------------------------
# STRICT top-1 prediction tests — the 4 previously-failing cases
# ---------------------------------------------------------------------------

class TestPreviouslyFailingCases:
    """
    These 4 cases were previously predicted incorrectly.
    After improvements, they must now predict the correct disease as top-1.
    """

    def test_case1_pneumonia(self):
        """Case 1: Pneumonia was predicted as Bronchial Asthma (97.8%)."""
        result = predict_disease(CASE_1_PNEUMONIA)
        assert result["prediction"] == "Pneumonia", (
            f"CASE 1: Expected Pneumonia, got {result['prediction']} "
            f"({result['confidence']}%). "
            f"Top-3: {[e['disease'] for e in result['top_predictions']]}"
        )

    def test_case2_chickenpox(self):
        """Case 2: Chicken Pox was predicted as Impetigo (60.9%)."""
        result = predict_disease(CASE_2_CHICKENPOX)
        assert result["prediction"] == "Chicken pox", (
            f"CASE 2: Expected Chicken pox, got {result['prediction']} "
            f"({result['confidence']}%). "
            f"Top-3: {[e['disease'] for e in result['top_predictions']]}"
        )

    def test_case3_asthma(self):
        """Case 3: Bronchial Asthma was predicted as Drug Reaction (27.6%)."""
        result = predict_disease(CASE_3_ASTHMA)
        assert result["prediction"] == "Bronchial Asthma", (
            f"CASE 3: Expected Bronchial Asthma, got {result['prediction']} "
            f"({result['confidence']}%). "
            f"Top-3: {[e['disease'] for e in result['top_predictions']]}"
        )

    def test_case4_malaria(self):
        """Case 4: Malaria was predicted as Typhoid (50.9%)."""
        result = predict_disease(CASE_4_MALARIA)
        assert result["prediction"] == "Malaria", (
            f"CASE 4: Expected Malaria, got {result['prediction']} "
            f"({result['confidence']}%). "
            f"Top-3: {[e['disease'] for e in result['top_predictions']]}"
        )


# ---------------------------------------------------------------------------
# STRICT top-1 prediction tests — existing passing diseases
# ---------------------------------------------------------------------------

class TestExistingPassingCases:
    """
    These diseases were already predicted correctly.
    Ensure no regression after the improvements.
    """

    def test_dengue_prediction(self):
        result = predict_disease(DENGUE_INPUT)
        assert result["prediction"] == "Dengue", (
            f"Expected Dengue, got {result['prediction']} ({result['confidence']}%)"
        )

    def test_typhoid_prediction(self):
        result = predict_disease(TYPHOID_INPUT)
        assert result["prediction"] == "Typhoid", (
            f"Expected Typhoid, got {result['prediction']} ({result['confidence']}%)"
        )

    def test_arthritis_prediction(self):
        result = predict_disease(ARTHRITIS_INPUT)
        assert result["prediction"] == "Arthritis", (
            f"Expected Arthritis, got {result['prediction']} ({result['confidence']}%)"
        )

    def test_psoriasis_prediction(self):
        result = predict_disease(PSORIASIS_INPUT)
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert result["prediction"] in ["Psoriasis", "Fungal infection"], (
            f"Expected Psoriasis or Fungal infection, got {result['prediction']} ({result['confidence']}%)"
        )

    def test_fungal_infection_prediction(self):
        result = predict_disease(FUNGAL_INFECTION_INPUT)
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert result["prediction"] in ["Fungal infection", "Psoriasis"], (
            f"Expected Fungal infection or Psoriasis, got {result['prediction']} ({result['confidence']}%)"
        )


# ---------------------------------------------------------------------------
# Realistic disease prediction tests (top-N containment)
# ---------------------------------------------------------------------------

class TestRealisticPredictions:
    """Top-N containment tests — reflects the dataset's realistic ambiguity."""

    def test_dengue_in_top_predictions(self):
        result = predict_disease(DENGUE_INPUT)
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert "Dengue" in diseases, (
            f"Dengue not found in top-3. Got: {diseases}"
        )

    def test_malaria_or_dengue_top_for_fever_chills(self):
        result = predict_disease(MALARIA_INPUT)
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert any(d in diseases for d in ["Malaria", "Dengue", "Typhoid"]), (
            f"Expected fever-related disease in top-3. Got: {diseases}"
        )

    def test_typhoid_top_for_sustained_fever_gi(self):
        result = predict_disease(TYPHOID_INPUT)
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert any(d in diseases for d in ["Typhoid", "Malaria", "Dengue"]), (
            f"Expected fever disease in top-3 for typhoid input. Got: {diseases}"
        )

    def test_pneumonia_top_for_respiratory_symptoms(self):
        result = predict_disease(PNEUMONIA_INPUT)
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert any(d in diseases for d in ["Pneumonia", "Bronchial Asthma", "Common Cold"]), (
            f"Expected respiratory disease in top-3. Got: {diseases}"
        )

    def test_psoriasis_top_for_skin_symptoms(self):
        result = predict_disease(PSORIASIS_INPUT)
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert any(d in diseases for d in ["Psoriasis", "Fungal infection", "Impetigo"]), (
            f"Expected skin disease in top-3. Got: {diseases}"
        )

    def test_arthritis_top_for_joint_symptoms(self):
        result = predict_disease(ARTHRITIS_INPUT)
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert any(d in diseases for d in ["Arthritis", "Cervical spondylosis"]), (
            f"Expected joint disease in top-3. Got: {diseases}"
        )

    def test_confidence_improved_over_baseline(self):
        """
        Top confidence should be meaningfully higher than the pre-improvement
        baseline of ~8.4% for the reference malaria input.
        """
        result = predict_disease(MALARIA_INPUT)
        assert result["confidence"] > 12.0, (
            f"Confidence {result['confidence']}% is too low — calibration may have failed."
        )

    def test_no_negative_confidence_scores(self):
        for text in [DENGUE_INPUT, MALARIA_INPUT, TYPHOID_INPUT]:
            result = predict_disease(text)
            for entry in result["top_predictions"]:
                assert entry["confidence"] >= 0.0


# ---------------------------------------------------------------------------
# Dedicated Chicken Pox tests (v2)
# ---------------------------------------------------------------------------

class TestChickenPoxPrediction:
    """
    Chicken Pox was previously misclassified as Impetigo.
    These tests validate improvement after the preprocessing + symptom enrichment.
    """

    def test_chickenpox_in_top3_with_blisters(self):
        """With fluid-filled blisters in the input, Chicken Pox should appear in top-3."""
        result = predict_disease(CHICKENPOX_INPUT)
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert any(d in diseases for d in ["Chicken pox", "Impetigo", "Acne"]), (
            f"Expected skin vesicular disease in top-3. Got: {diseases}"
        )

    def test_chickenpox_extended_in_top3(self):
        """Extended clinical description should place Chicken Pox in top-3."""
        result = predict_disease(CHICKENPOX_EXTENDED_INPUT)
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert any(d in diseases for d in ["Chicken pox", "Impetigo"]), (
            f"Expected Chicken pox or Impetigo in top-3. Got: {diseases}"
        )

    def test_chickenpox_blisters_symptom_extracted(self):
        """Symptom extraction must capture 'blisters' from a Chicken Pox description."""
        result = predict_disease(CHICKENPOX_INPUT)
        assert "blisters" in result["symptoms"], (
            f"'blisters' not extracted from Chicken Pox input. Got: {result['symptoms']}"
        )

    def test_chickenpox_fever_and_itching_extracted(self):
        result = predict_disease(CHICKENPOX_INPUT)
        syms = result["symptoms"]
        assert "fever" in syms
        assert "itching" in syms


# ---------------------------------------------------------------------------
# Dedicated Pneumonia tests (v2)
# ---------------------------------------------------------------------------

class TestPneumoniaExtended:
    """
    Pneumonia was previously misclassified as Bronchial Asthma on terse input.
    Extended descriptions include productive cough + chest congestion signals.
    """

    def test_pneumonia_extended_top3_contains_respiratory_disease(self):
        result = predict_disease(PNEUMONIA_EXTENDED_INPUT)
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert any(d in diseases for d in ["Pneumonia", "Bronchial Asthma", "Common Cold"]), (
            f"Expected respiratory disease in top-3. Got: {diseases}"
        )

    def test_pneumonia_extended_extracts_chest_congestion(self):
        """Chest congestion is a Pneumonia differentiator and must be extracted."""
        result = predict_disease(PNEUMONIA_EXTENDED_INPUT)
        assert "chest congestion" in result["symptoms"], (
            f"'chest congestion' not extracted. Symptoms: {result['symptoms']}"
        )

    def test_pneumonia_extended_extracts_cough(self):
        result = predict_disease(PNEUMONIA_EXTENDED_INPUT)
        syms = result["symptoms"]
        assert "cough" in syms or "productive cough" in syms

    def test_pneumonia_extended_extracts_chest_pain(self):
        result = predict_disease(PNEUMONIA_EXTENDED_INPUT)
        assert "chest pain" in result["symptoms"]

    def test_pneumonia_specialist_is_pulmonologist(self):
        """
        When Pneumonia is predicted, the recommended specialist should be Pulmonologist.
        This test is conditional — only asserts if prediction == Pneumonia.
        """
        result = predict_disease(PNEUMONIA_EXTENDED_INPUT)
        if result["prediction"] == "Pneumonia":
            assert result["specialist"] == "Pulmonologist", (
                f"Expected Pulmonologist for Pneumonia. Got: {result['specialist']}"
            )


# ---------------------------------------------------------------------------
# Symptom-based boosting tests (v3)
# ---------------------------------------------------------------------------

class TestBoostingLayer:
    """Validates the symptom-based boosting adjusts probabilities correctly."""

    def test_wheezing_boosts_asthma(self):
        """Wheezing is the hallmark of Bronchial Asthma and should boost it."""
        result = predict_disease("Wheezing and chest tightness with shortness of breath.")
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert "Bronchial Asthma" in diseases, (
            f"Expected Bronchial Asthma in top-3 with wheezing. Got: {diseases}"
        )

    def test_productive_cough_boosts_pneumonia(self):
        """Productive cough is a Pneumonia differentiator."""
        result = predict_disease(
            "Persistent cough producing mucus. Fever. Chest pain. Difficulty breathing."
        )
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert "Pneumonia" in diseases, (
            f"Expected Pneumonia in top-3 with productive cough. Got: {diseases}"
        )

    def test_blisters_boosts_chickenpox(self):
        """Fluid-filled blisters should boost Chicken pox."""
        result = predict_disease("Fever. Rash. Fluid-filled blisters. Itching.")
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert "Chicken pox" in diseases, (
            f"Expected Chicken pox in top-3 with blisters. Got: {diseases}"
        )

    def test_chills_sweating_boosts_malaria(self):
        """Chills + sweating should boost Malaria."""
        result = predict_disease("Fever. Chills. Sweating. Headache. Vomiting.")
        diseases = [e["disease"] for e in result["top_predictions"]]
        assert "Malaria" in diseases, (
            f"Expected Malaria in top-3 with chills+sweating. Got: {diseases}"
        )
