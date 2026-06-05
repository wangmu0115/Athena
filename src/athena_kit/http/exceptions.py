from typing import Any

import httpx


class HttpClientError(Exception):
    """Base exception for HTTP client errors."""


class HttpTimeoutError(HttpClientError):
    """Raised when an HTTP request times out."""


class HttpRequestError(HttpClientError):
    """Raised when a network-level error occurs (connection, DNS, etc.)."""


class HttpResponseError(HttpClientError):
    """Raised when the HTTP response status code indicates failure."""

    def __init__(self, status_code: int, message: str, response: httpx.Response):
        self.status_code = status_code
        self.response = response
        self.method = response.request.method
        self.url = str(response.request.url)
        super().__init__(f"HTTP response error: status_code={status_code}, message={message}")


class PayloadError(HttpClientError):
    """Base exception for response payload processing errors."""


class InvalidPayloadError(PayloadError):
    """The result of response.json() is not a dict."""


class PayloadBizStatusError(PayloadError):
    """Exception in response payload business status error."""

    def __init__(
        self,
        message: str,
        *,
        code: Any = None,
        payload: dict[str, Any] | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.payload = payload
