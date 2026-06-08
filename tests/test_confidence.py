"""
Confidence Level Helper Tests
=============================
Validates the get_confidence_level() threshold logic in predictor.py.
"""

import pytest
from backend.services.predictor import get_confidence_level


class TestGetConfidenceLevel:

    # Boundary: High
    def test_exactly_70_is_high(self):
        assert get_confidence_level(70.0) == "High"

    def test_above_70_is_high(self):
        assert get_confidence_level(85.5) == "High"
        assert get_confidence_level(100.0) == "High"
        assert get_confidence_level(70.01) == "High"

    # Boundary: Medium
    def test_exactly_40_is_medium(self):
        assert get_confidence_level(40.0) == "Medium"

    def test_between_40_and_70_is_medium(self):
        assert get_confidence_level(55.0) == "Medium"
        assert get_confidence_level(40.01) == "Medium"
        assert get_confidence_level(69.99) == "Medium"

    # Boundary: Low
    def test_below_40_is_low(self):
        assert get_confidence_level(39.99) == "Low"
        assert get_confidence_level(25.0) == "Low"
        assert get_confidence_level(8.4) == "Low"
        assert get_confidence_level(0.0) == "Low"

    def test_returns_string(self):
        result = get_confidence_level(50.0)
        assert isinstance(result, str)

    def test_valid_values_only(self):
        valid = {"High", "Medium", "Low"}
        for v in [0, 10, 39.99, 40, 55, 70, 85, 100]:
            assert get_confidence_level(v) in valid
