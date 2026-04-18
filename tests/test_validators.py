"""Tests for input validation utilities."""

import pytest
from backend.utils.validators import (
    validate_budget,
    validate_dietary_preferences,
    validate_servings,
)


class TestBudgetValidation:
    """Test suite for budget validation."""

    def test_valid_budget(self):
        """Test valid budget amounts."""
        assert validate_budget(50.0) is True
        assert validate_budget(100) is True
        assert validate_budget(0.01) is True

    def test_invalid_budget_negative(self):
        """Test that negative budgets are rejected."""
        with pytest.raises(ValueError, match="greater than 0"):
            validate_budget(-10.0)

    def test_invalid_budget_zero(self):
        """Test that zero budget is rejected."""
        with pytest.raises(ValueError, match="greater than 0"):
            validate_budget(0)

    def test_invalid_budget_exceeds_max(self):
        """Test that budget exceeding max is rejected."""
        with pytest.raises(ValueError, match="exceeds maximum"):
            validate_budget(11000)

    def test_invalid_budget_non_numeric(self):
        """Test that non-numeric budget is rejected."""
        with pytest.raises(ValueError, match="must be a number"):
            validate_budget("fifty")


class TestDietaryPreferencesValidation:
    """Test suite for dietary preferences validation."""

    def test_valid_preferences(self):
        """Test valid dietary preferences."""
        assert validate_dietary_preferences(["vegetarian"]) is True
        assert validate_dietary_preferences(["vegan", "gluten-free"]) is True
        assert validate_dietary_preferences(["keto", "dairy-free", "nut-free"]) is True

    def test_empty_preferences_valid(self):
        """Test that empty preference list is valid."""
        assert validate_dietary_preferences([]) is True

    def test_invalid_preference(self):
        """Test that invalid preferences are rejected."""
        with pytest.raises(ValueError, match="Invalid dietary preferences"):
            validate_dietary_preferences(["invalid-diet"])

    def test_mixed_valid_invalid_preferences(self):
        """Test that mixed valid/invalid preferences are rejected."""
        with pytest.raises(ValueError, match="Invalid dietary preferences"):
            validate_dietary_preferences(["vegetarian", "invalid-diet"])

    def test_non_list_preferences(self):
        """Test that non-list preferences are rejected."""
        with pytest.raises(ValueError, match="must be a list"):
            validate_dietary_preferences("vegetarian")


class TestServingsValidation:
    """Test suite for servings validation."""

    def test_valid_servings(self):
        """Test valid serving counts."""
        assert validate_servings(1) is True
        assert validate_servings(4) is True
        assert validate_servings(100) is True

    def test_invalid_servings_zero(self):
        """Test that zero servings is rejected."""
        with pytest.raises(ValueError, match="at least 1"):
            validate_servings(0)

    def test_invalid_servings_negative(self):
        """Test that negative servings are rejected."""
        with pytest.raises(ValueError, match="at least 1"):
            validate_servings(-5)

    def test_invalid_servings_exceeds_max(self):
        """Test that servings exceeding max are rejected."""
        with pytest.raises(ValueError, match="exceeds maximum"):
            validate_servings(101)

    def test_invalid_servings_non_integer(self):
        """Test that non-integer servings are rejected."""
        with pytest.raises(ValueError, match="must be an integer"):
            validate_servings(3.5)
