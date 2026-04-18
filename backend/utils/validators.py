"""Input validation utilities for user inputs."""

from typing import List, Optional


def validate_budget(budget: float) -> bool:
    """
    Validate meal planning budget.
    
    Args:
        budget: Budget amount in dollars
        
    Returns:
        True if valid, raises ValueError otherwise
    """
    if not isinstance(budget, (int, float)):
        raise ValueError("Budget must be a number")
    if budget <= 0:
        raise ValueError("Budget must be greater than 0")
    if budget > 10000:  # Reasonable upper limit
        raise ValueError("Budget exceeds maximum allowed amount")
    return True


def validate_dietary_preferences(preferences: List[str]) -> bool:
    """
    Validate dietary preference selections.
    
    Args:
        preferences: List of dietary preference strings
        
    Returns:
        True if valid, raises ValueError otherwise
    """
    allowed = {
        "vegetarian",
        "vegan",
        "gluten-free",
        "dairy-free",
        "nut-free",
        "keto",
        "paleo",
        "low-carb",
        "mediterranean",
        "low-sodium",
    }
    
    if not isinstance(preferences, list):
        raise ValueError("Preferences must be a list")
    
    invalid = set(preferences) - allowed
    if invalid:
        raise ValueError(f"Invalid dietary preferences: {invalid}")
    
    return True


def validate_servings(servings: int) -> bool:
    """
    Validate number of servings.
    
    Args:
        servings: Number of servings
        
    Returns:
        True if valid, raises ValueError otherwise
    """
    if not isinstance(servings, int):
        raise ValueError("Servings must be an integer")
    if servings < 1:
        raise ValueError("Servings must be at least 1")
    if servings > 100:
        raise ValueError("Servings exceeds maximum of 100")
    return True
