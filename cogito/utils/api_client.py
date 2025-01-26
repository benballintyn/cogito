"""
A base class for interacting with APIs with retry, rate-limiting, and logging support.
"""

import asyncio
from typing import Any, Dict, Optional

import httpx
from loguru import logger

from cogito.utils.retry import async_retry


class APIClient:
    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        rate_limit_delay: float = 0.5,
    ):
        """
        Initialize the API client.

        Args:
            base_url (str): The base URL for the API.
            headers (Optional[Dict[str, str]]): Default headers to include with every request.
            rate_limit_delay (float): Delay (in seconds) between consecutive requests to prevent rate-limiting.
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.rate_limit_delay = rate_limit_delay
        self._last_request_time = 0.0

    @async_retry(max_retries=3, backoff_factor=1.0, exceptions=(httpx.RequestError,))
    async def _request(
        self, method: str, endpoint: str, **kwargs: Any
    ) -> httpx.Response:
        """
        Make an HTTP request with retry and rate-limiting.

        Args:
            method (str): HTTP method (e.g., "GET", "POST").
            endpoint (str): API endpoint relative to the base URL.
            **kwargs: Additional arguments to pass to the `httpx.request` method.

        Returns:
            httpx.Response: The response object.

        Raises:
            httpx.RequestError: If the request fails after retries.
        """
        # Respect rate-limiting
        now = asyncio.get_event_loop().time()
        if now - self._last_request_time < self.rate_limit_delay:
            delay = self.rate_limit_delay - (now - self._last_request_time)
            logger.debug(f"Rate limiting: delaying request by {delay:.2f}s")
            await asyncio.sleep(delay)

        # Make the HTTP request
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            logger.info(f"Sending {method} request to {url}")
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method, url, headers=self.headers, **kwargs
                )
                response.raise_for_status()  # Raise HTTP errors if status is 4xx/5xx
                logger.info(
                    f"Received response: {response.status_code} {response.text}"
                )
                return response
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise
        finally:
            self._last_request_time = asyncio.get_event_loop().time()

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request."""
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Make a POST request."""
        return await self._request("POST", endpoint, json=json)

    async def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Make a PUT request."""
        return await self._request("PUT", endpoint, json=json)

    async def delete(self, endpoint: str) -> Any:
        """Make a DELETE request."""
        return await self._request("DELETE", endpoint)
