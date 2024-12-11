import requests
from typing import Optional, Any


class APIClient:
    def __init__(self, base_url: str, headers: Optional[dict[str, str]] = None):
        """
        Initialize the API client.

        :param base_url: Base URL for the API.
        :param headers: Optional headers to include in all requests.
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}

    def _build_url(self, endpoint: str) -> str:
        """Helper method to construct full URL from base URL and endpoint."""
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make a generic HTTP request.

        :param method: HTTP method ('GET', 'POST', 'PUT', 'DELETE').
        :param endpoint: API endpoint.
        :param kwargs: Additional arguments to pass to `requests` methods (e.g., json, params, data).
        :return: Response object.
        """
        url = self._build_url(endpoint)
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response

    def get(
        self, endpoint: str, params: Optional[dict[str, Any]] = None
    ) -> requests.Response:
        """
        Send a GET request.

        :param endpoint: API endpoint.
        :param params: Query parameters.
        :return: Response object.
        """
        return self._request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
    ) -> requests.Response:
        """
        Send a POST request.

        :param endpoint: API endpoint.
        :param json: JSON payload.
        :param data: Form data payload.
        :return: Response object.
        """
        return self._request("POST", endpoint, json=json, data=data)

    def put(
        self,
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
    ) -> requests.Response:
        """
        Send a PUT request.

        :param endpoint: API endpoint.
        :param json: JSON payload.
        :param data: Form data payload.
        :return: Response object.
        """
        return self._request("PUT", endpoint, json=json, data=data)

    def delete(self, endpoint: str) -> requests.Response:
        """
        Send a DELETE request.

        :param endpoint: API endpoint.
        :return: Response object.
        """
        return self._request("DELETE", endpoint)
