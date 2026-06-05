from typing import Any


class PayloadError(Exception):
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
