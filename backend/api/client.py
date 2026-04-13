"""Generic API client wrapper for external service integrations."""

import aiohttp
from typing import Optional, Dict, Any
from .auth import APIAuthManager


class APIClient:
    """
    Generic API client for making authenticated requests to external services.
    Integrates with token_manager for secure credential handling.
    """

    def __init__(self, base_url: str, auth_manager: APIAuthManager):
        self.base_url = base_url.rstrip('/')
        self.auth_manager = auth_manager
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get(
        self,
        endpoint: str,
        user_id: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make authenticated GET request."""
        headers = await self._get_headers(user_id)
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        async with self.session.get(url, headers=headers, params=params, **kwargs) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def post(
        self,
        endpoint: str,
        user_id: str,
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make authenticated POST request."""
        headers = await self._get_headers(user_id)
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        async with self.session.post(url, headers=headers, json=data, **kwargs) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def _get_headers(self, user_id: str) -> Dict[str, str]:
        """Get authorization headers with valid token."""
        token = await self.auth_manager.get_valid_token(user_id)
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
