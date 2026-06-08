"""
Symptom Extractor Tests — v2
============================
Validates that the synonym knowledge base correctly extracts canonical symptom
names from realistic free-text patient descriptions for all target diseases.

v2 additions (matching symptom_extractor.py v2):
  - TestNewCanonicals — pain_behind_eyes, blisters, chest_congestion, silvery_scales
  - TestExpandedAliases — productive cough, body aches, joint stiffness / morning stiffness
  - TestChickenpoxVsRash — ensures "blisters" and "rash" are now distinct canonicals
  - Extended disease-scenario tests for Dengue (eye pain), Pneumonia (productive cough)
"""

import pytest
from backend.services.symptom_extractor import extract_symptoms


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def symptoms_contain(result: list, *expected: str) -> bool:
    """Check that all expected canonical symptoms are in the result list."""
    return all(s in result for s in expected)


# ---------------------------------------------------------------------------
# Core synonym mapping tests (v1 coverage retained)
# ---------------------------------------------------------------------------

class TestSynonymMappings:

    def test_fever_variants(self):
        assert "fever" in extract_symptoms("I have a high fever")
        assert "fever" in extract_symptoms("I feel feverish and hot")
        assert "fever" in extract_symptoms("My temperature is very high")
        assert "fever" in extract_symptoms("I have pyrexia and feel unwell")

    def test_fatigue_variants(self):
        assert "fatigue" in extract_symptoms("I feel exhausted and drained")
        assert "fatigue" in extract_symptoms("I feel extreme weakness")
        assert "fatigue" in extract_symptoms("I am tired and have low energy")
        assert "fatigue" in extract_symptoms("I feel lethargic all day")

    def test_sweating_variants(self):
        assert "sweating" in extract_symptoms("I have excessive sweating")
        assert "sweating" in extract_symptoms("I wake up with night sweats")
        assert "sweating" in extract_symptoms("I am perspiring heavily")

    def test_muscle_pain_variants(self):
        assert "muscle pain" in extract_symptoms("I have severe muscle pain")
        assert "muscle pain" in extract_symptoms("I have body aches all over")
        assert "muscle pain" in extract_symptoms("I experience body pain daily")
        assert "muscle pain" in extract_symptoms("My muscles are aching badly")
        assert "muscle pain" in extract_symptoms("I have myalgia")

    def test_headache_variants(self):
        assert "headache" in extract_symptoms("I have a bad headache")
        assert "headache" in extract_symptoms("I suffer from migraines")
        assert "headache" in extract_symptoms("I have a throbbing head pain")

    def test_chills_variants(self):
        assert "chills" in extract_symptoms("I have chills and shivering")
        assert "chills" in extract_symptoms("I experience rigors frequently")

    def test_vomiting_variants(self):
        assert "vomiting" in extract_symptoms("I have been vomiting")
        assert "vomiting" in extract_symptoms("I keep throwing up")
        assert "vomiting" in extract_symptoms("I have been retching all day")

    def test_rash_variants(self):
        assert "rash" in extract_symptoms("I have a skin rash on my arms")
        assert "rash" in extract_symptoms("I have hives on my body")
        assert "rash" in extract_symptoms("I have scaly patches on my skin")

    def test_joint_pain_variants(self):
        assert "joint pain" in extract_symptoms("I have joint pain in my knees")
        assert "joint pain" in extract_symptoms("I have arthralgia")
        assert "joint pain" in extract_symptoms("My joints are stiff and swollen")

    def test_cough_variants(self):
        assert "cough" in extract_symptoms("I have a persistent dry cough")
        assert "cough" in extract_symptoms("I have been coughing for a week")

    def test_shortness_of_breath_variants(self):
        assert "shortness of breath" in extract_symptoms("I have shortness of breath")
        assert "shortness of breath" in extract_symptoms("I am breathless")
        assert "shortness of breath" in extract_symptoms("I have difficulty breathing")

    def test_diarrhea_variants(self):
        assert "diarrhea" in extract_symptoms("I have diarrhea")
        assert "diarrhea" in extract_symptoms("I have loose stools")
        assert "diarrhea" in extract_symptoms("I have watery stools frequently")

    def test_itching_variants(self):
        assert "itching" in extract_symptoms("My skin is very itchy")
        assert "itching" in extract_symptoms("I have intense itching on my scalp")

    def test_abdominal_pain_variants(self):
        assert "abdominal pain" in extract_symptoms("I have stomach pain")
        assert "abdominal pain" in extract_symptoms("I have abdominal cramps")
        assert "abdominal pain" in extract_symptoms("I have belly pain")


# ---------------------------------------------------------------------------
# NEW: v2 canonical symptom tests
# ---------------------------------------------------------------------------

class TestNewCanonicals:
    """Tests for the 4 new canonical symptoms added in v2."""

    # --- pain behind eyes ---
    def test_pain_behind_eyes_exact(self):
        assert "pain behind eyes" in extract_symptoms(
            "I have a severe headache and pain behind my eyes."
        )

    def test_pain_behind_eyes_retro_orbital(self):
        assert "pain behind eyes" in extract_symptoms(
            "I experience retro-orbital pain and high fever."
        )

    def test_pain_behind_eyes_around_eyes(self):
        assert "pain behind eyes" in extract_symptoms(
            "There is pain around the eyes and my head is pounding."
        )

    def test_pain_behind_eyes_exact_phrase(self):
        assert "pain behind eyes" in extract_symptoms(
            "pain behind the eyes is very bad"
        )

    # --- blisters (new distinct canonical) ---
    def test_blisters_fluid_filled_hyphenated(self):
        assert "blisters" in extract_symptoms(
            "I have fluid-filled blisters all over my body."
        )

    def test_blisters_fluid_filled_no_hyphen(self):
        assert "blisters" in extract_symptoms(
            "I have fluid filled blisters on my skin."
        )

    def test_blisters_water_blisters(self):
        assert "blisters" in extract_symptoms(
            "I notice water blisters appearing on my arms."
        )

    def test_blisters_vesicles(self):
        assert "blisters" in extract_symptoms(
            "The doctor said I have vesicles on my skin."
        )

    def test_blisters_blistering(self):
        assert "blisters" in extract_symptoms(
            "My skin is blistering in several places."
        )

    # --- chest congestion ---
    def test_chest_congestion_exact(self):
        assert "chest congestion" in extract_symptoms(
            "I have chest congestion and a productive cough."
        )

    def test_chest_congestion_congested_chest(self):
        assert "chest congestion" in extract_symptoms(
            "My chest feels congested and it hurts to breathe."
        )

    def test_chest_congestion_mucus_in_chest(self):
        assert "chest congestion" in extract_symptoms(
            "There is mucus in my chest and I can't breathe well."
        )

    def test_chest_congestion_fullness(self):
        assert "chest congestion" in extract_symptoms(
            "I feel chest fullness and find it hard to breathe deeply."
        )

    # --- silvery scales ---
    def test_silvery_scales_exact(self):
        assert "silvery scales" in extract_symptoms(
            "My skin has silvery scales on the elbows."
        )

    def test_silvery_scales_silver_like_dusting(self):
        assert "silvery scales" in extract_symptoms(
            "There is a silver-like dusting on my skin."
        )

    def test_silvery_scales_silver_like_dusting_no_hyphen(self):
        assert "silvery scales" in extract_symptoms(
            "There is a silver like dusting on my lower back."
        )

    def test_silvery_scales_scaly_plaques(self):
        assert "silvery scales" in extract_symptoms(
            "The dermatologist said I have scaly plaques on my scalp."
        )


# ---------------------------------------------------------------------------
# NEW: v2 expanded alias tests
# ---------------------------------------------------------------------------

class TestExpandedAliases:
    """Tests for aliases added to existing canonicals in v2."""

    # --- cough: productive/phlegm/mucus variants ---
    def test_productive_cough(self):
        assert "cough" in extract_symptoms("I have a productive cough every morning.")

    def test_cough_with_phlegm(self):
        assert "cough" in extract_symptoms("I have a cough with phlegm.")

    def test_coughing_up_mucus(self):
        assert "cough" in extract_symptoms("I have been coughing up mucus.")

    def test_coughing_up_phlegm(self):
        assert "cough" in extract_symptoms("I keep coughing up phlegm.")

    def test_mucus_cough(self):
        assert "cough" in extract_symptoms("I have a mucus cough that won't stop.")

    def test_phlegm_cough(self):
        assert "cough" in extract_symptoms("My phlegm cough is getting worse.")

    def test_cough_producing_mucus(self):
        assert "cough" in extract_symptoms(
            "Persistent cough producing mucus all day."
        )

    # --- muscle pain: body aches ---
    def test_body_aches(self):
        assert "muscle pain" in extract_symptoms(
            "I have body aches all over from the flu."
        )

    def test_aches_all_over(self):
        assert "muscle pain" in extract_symptoms(
            "I have aches all over and feel terrible."
        )

    def test_aches_and_pains(self):
        assert "muscle pain" in extract_symptoms(
            "I have aches and pains throughout my body."
        )

    # --- joint pain: stiffness variants ---
    def test_joint_stiffness(self):
        assert "joint pain" in extract_symptoms(
            "I suffer from joint stiffness every morning."
        )

    def test_morning_stiffness(self):
        assert "joint pain" in extract_symptoms(
            "I have morning stiffness in my fingers and wrists."
        )

    def test_stiffness_in_joints(self):
        assert "joint pain" in extract_symptoms(
            "There is significant stiffness in joints after sitting."
        )

    def test_joints_feel_stiff(self):
        assert "joint pain" in extract_symptoms(
            "My joints feel stiff when I wake up."
        )


# ---------------------------------------------------------------------------
# NEW: Blisters vs Rash disambiguation
# ---------------------------------------------------------------------------

class TestChickenpoxVsRash:
    """
    Ensure blisters and rash are distinct canonicals.
    Chicken Pox inputs should trigger "blisters" (not just "rash").
    Psoriasis/Impetigo inputs should trigger "rash" (not "blisters").
    """

    def test_blisters_is_separate_canonical_from_rash(self):
        result = extract_symptoms("I have fluid-filled blisters on my body.")
        assert "blisters" in result
        # "rash" should NOT be triggered by fluid-filled blisters alone
        assert "rash" not in result

    def test_scaly_patches_map_to_rash_not_blisters(self):
        result = extract_symptoms("I have scaly patches and peeling skin.")
        assert "rash" in result
        assert "blisters" not in result

    def test_chickenpox_input_triggers_both_rash_and_blisters(self):
        text = "I have a fever, a rash all over my body, and fluid-filled blisters."
        result = extract_symptoms(text)
        assert "rash" in result
        assert "blisters" in result

    def test_impetigo_sores_do_not_trigger_blisters(self):
        text = "I have red sores on my face. The sores are painful."
        result = extract_symptoms(text)
        assert "blisters" not in result


# ---------------------------------------------------------------------------
# Disease-specific scenario tests (v1 retained + extended)
# ---------------------------------------------------------------------------

class TestDengueSymptoms:

    def test_dengue_typical_description(self):
        text = (
            "I have a high fever with severe headache and muscle pain. "
            "I also have chills and have been vomiting."
        )
        result = extract_symptoms(text)
        assert symptoms_contain(result, "fever", "headache", "muscle pain", "chills", "vomiting")

    def test_dengue_rash_variant(self):
        text = "I have fever, skin rash, and joint pain all over my body."
        result = extract_symptoms(text)
        assert symptoms_contain(result, "fever", "rash", "joint pain")

    def test_dengue_with_eye_pain(self):
        """Dengue differentiator — retro-orbital pain should be captured."""
        text = (
            "I have a sudden high fever with severe headache and pain behind the eyes. "
            "I also have joint pain, muscle pain, and a skin rash."
        )
        result = extract_symptoms(text)
        assert symptoms_contain(result, "fever", "headache", "pain behind eyes", "joint pain", "muscle pain", "rash")


class TestMalariaSymptoms:

    def test_malaria_typical_description(self):
        text = (
            "I have recurring episodes of high fever followed by chills "
            "and excessive sweating. I feel extremely weak and exhausted. "
            "I also experience headaches, muscle pain, and occasional vomiting."
        )
        result = extract_symptoms(text)
        assert symptoms_contain(
            result, "fever", "chills", "sweating", "fatigue",
            "headache", "muscle pain", "vomiting"
        )

    def test_malaria_minimal(self):
        text = "I have fever and shivering, I feel very weak."
        result = extract_symptoms(text)
        assert symptoms_contain(result, "fever", "chills", "fatigue")


class TestTyphoidSymptoms:

    def test_typhoid_typical_description(self):
        text = (
            "I have sustained high fever and weakness. "
            "I also have stomach pain and loss of appetite."
        )
        result = extract_symptoms(text)
        assert symptoms_contain(result, "fever", "fatigue", "abdominal pain", "loss of appetite")


class TestPneumoniaSymptoms:

    def test_pneumonia_typical_description(self):
        text = (
            "I have a persistent cough with difficulty breathing and chest pain. "
            "I also have a fever and feel very tired."
        )
        result = extract_symptoms(text)
        assert symptoms_contain(
            result, "cough", "shortness of breath", "chest pain", "fever", "fatigue"
        )

    def test_pneumonia_productive_cough_and_congestion(self):
        """
        Pneumonia differentiator: productive cough + chest congestion
        should both be detected in a realistic Pneumonia description.
        """
        text = (
            "Persistent cough producing mucus, chest pain, fever, chills, "
            "difficulty breathing. My chest feels congested."
        )
        result = extract_symptoms(text)
        assert symptoms_contain(result, "cough", "chest pain", "fever", "chills", "shortness of breath", "chest congestion")

    def test_pneumonia_coughing_up_phlegm(self):
        text = (
            "I have been coughing up phlegm for three days. "
            "I have chest pain, high fever, and difficulty breathing."
        )
        result = extract_symptoms(text)
        assert symptoms_contain(result, "cough", "chest pain", "fever", "shortness of breath")


class TestChickenpoxSymptoms:

    def test_chickenpox_typical_description(self):
        text = (
            "I have a high fever and my skin is very itchy. "
            "I have a rash with fluid-filled blisters spreading all over."
        )
        result = extract_symptoms(text)
        assert symptoms_contain(result, "fever", "itching", "rash", "blisters")

    def test_chickenpox_blisters_detected(self):
        """The key differentiator for Chicken Pox must always be extracted."""
        text = "Fever, rash, itching, fluid-filled blisters."
        result = extract_symptoms(text)
        assert "blisters" in result
        assert "fever" in result
        assert "rash" in result
        assert "itching" in result


class TestPsoriasisSymptoms:

    def test_psoriasis_typical_description(self):
        text = (
            "I have red, itchy scaly patches on my arms and legs. "
            "My skin is peeling and the rash is spreading."
        )
        result = extract_symptoms(text)
        assert symptoms_contain(result, "itching", "rash")

    def test_psoriasis_silvery_scales(self):
        """Psoriasis differentiator — silvery scales should be captured."""
        text = (
            "I have red, itchy patches on my skin. "
            "There is a silver-like dusting on my lower back and scalp."
        )
        result = extract_symptoms(text)
        assert "silvery scales" in result


class TestArthritisSymptoms:

    def test_arthritis_typical_description(self):
        text = (
            "I have joint pain in my fingers, wrists, and knees. "
            "The joints feel stiff in the morning and I feel fatigued."
        )
        result = extract_symptoms(text)
        assert symptoms_contain(result, "joint pain", "fatigue")

    def test_arthritis_morning_stiffness(self):
        """Morning stiffness is a clinical hallmark of rheumatoid arthritis."""
        text = (
            "My joints are swollen and I have morning stiffness every day. "
            "I feel fatigued and the pain worsens with movement."
        )
        result = extract_symptoms(text)
        assert symptoms_contain(result, "joint pain", "fatigue")


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_empty_string(self):
        assert extract_symptoms("") == []

    def test_no_symptoms(self):
        result = extract_symptoms("I am feeling great today, no issues at all.")
        assert result == []

    def test_no_duplicates(self):
        text = "I have fever and high fever and feverish symptoms."
        result = extract_symptoms(text)
        assert result.count("fever") == 1

    def test_returns_list(self):
        result = extract_symptoms("I have a cough")
        assert isinstance(result, list)

    def test_case_insensitive(self):
        assert "fever" in extract_symptoms("I have FEVER")
        assert "fever" in extract_symptoms("I have Fever")
        assert "fever" in extract_symptoms("I have FEVERISH symptoms")

    def test_blisters_case_insensitive(self):
        assert "blisters" in extract_symptoms("I have FLUID-FILLED BLISTERS")

    def test_silvery_scales_case_insensitive(self):
        assert "silvery scales" in extract_symptoms("SILVERY SCALES on my elbows")

    def test_multiple_new_canonicals_in_one_text(self):
        """All four new canonicals can appear in a complex description."""
        text = (
            "I have fever, pain behind the eyes, fluid-filled blisters, "
            "chest congestion, and silvery scales on my elbows."
        )
        result = extract_symptoms(text)
        assert symptoms_contain(
            result,
            "fever", "pain behind eyes", "blisters",
            "chest congestion", "silvery scales"
        )
