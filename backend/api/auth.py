"""Authentication manager for API clients.

Integrates with token_manager.py for secure token storage and renewal.
"""

from typing import Optional
from backend.token_manager import get_token, refresh_access_token
import asyncio


class APIAuthManager:
    """
    Manages authentication for API clients.
    Uses the existing token_manager to store and refresh tokens securely.
    """

    def __init__(self, refresh_func=None):
        """
        Initialize auth manager.
        
        Args:
            refresh_func: Async function to refresh token: 
                         async def refresh_func(refresh_token: str) -> tuple(access_token, refresh_token, expires_in)
        """
        self.refresh_func = refresh_func

    async def get_valid_token(self, user_id: str) -> str:
        """
        Get a valid access token, refreshing if needed.
        
        Args:
            user_id: The user ID to get token for
            
        Returns:
            Valid access token
            
        Raises:
            ValueError: If token is expired and refresh fails
        """
        # Run synchronous token_manager in async context
        loop = asyncio.get_event_loop()
        token = await loop.run_in_executor(None, lambda: get_token(user_id))
        
        if token == 'expired':
            if self.refresh_func:
                new_token = await self.refresh_func(user_id)
                return new_token
            else:
                raise ValueError(f"Token expired for user {user_id} and no refresh function provided")
        
        if not token:
            raise ValueError(f"No token found for user {user_id}")
        
        return token
