"""Example tests for API client usage."""

import pytest
import asyncio
from backend.api.client import APIClient
from backend.api.auth import APIAuthManager


@pytest.mark.asyncio
async def test_api_client_initialization():
    """Test API client can be initialized."""
    auth_manager = APIAuthManager()
    client = APIClient("https://api.example.com", auth_manager)
    
    assert client.base_url == "https://api.example.com"
    assert client.auth_manager == auth_manager


@pytest.mark.asyncio
async def test_api_client_context_manager():
    """Test API client can be used as async context manager."""
    auth_manager = APIAuthManager()
    
    async with APIClient("https://api.example.com", auth_manager) as client:
        assert client.session is not None


# TODO: Add integration tests with mock responses
# Example:
# @pytest.mark.asyncio
# async def test_get_recipes_via_api():
#     """Test fetching recipes through API client."""
#     auth_manager = APIAuthManager(refresh_func=mock_refresh)
#     async with APIClient("https://api.recipes.com", auth_manager) as client:
#         recipes = await client.get("recipes", user_id="user123", params={"limit": 10})
#         assert isinstance(recipes, dict)
#         assert "data" in recipes
