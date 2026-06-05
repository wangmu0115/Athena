from collections.abc import Callable, Sequence
from typing import Any, overload

from httpx import Response

from athena_kit.http import InvalidPayloadError, PayloadBizStatusError

Payload = dict[str, Any]
EnsureSuccess = Callable[[Payload], None]

_MISSING = object()


def ensure_biz_code_success(
    payload: Payload,
    *,
    code_key: str = "code",
    success_codes: Sequence[int | str] = (0,),
    message_key: str = "message",
) -> None:
    """Validate whether the response payload indicates success.

    This function checks business-level success based on a status code field.
    """
    code = payload.get(code_key)
    if code is None:
        raise PayloadBizStatusError(f"Missing biz status field: {code_key}", code=None, payload=payload)

    if code not in success_codes:
        message = payload.get(message_key, f"Missing error message field: {message_key}")
        raise PayloadBizStatusError(f"Request failed: code={code}, message={message}", code=code, payload=payload)


def make_biz_code_validator(
    *,
    code_key: str = "code",
    success_codes: Sequence[int | str] = (0,),
    message_key: str = "message",
) -> EnsureSuccess:
    """Create a payload status code success validator.

    This factory is useful when different APIs use different response
    conventions, such as `code/message`, `code/msg`, `status/msg`, or `err_no/err_msg`.
    """

    def _ensure_success(payload: Payload) -> None:
        ensure_biz_code_success(
            payload,
            code_key=code_key,
            success_codes=success_codes,
            message_key=message_key,
        )

    return _ensure_success


@overload
def extract_payload(
    response: Response,
    keys: None,
    *,
    ensure_success: EnsureSuccess | None = ...,
    deep: bool = ...,
) -> None: ...


@overload
def extract_payload(
    response: Response,
    keys: str,
    *,
    ensure_success: EnsureSuccess | None = ...,
    deep: bool = ...,
) -> Any: ...


@overload
def extract_payload(
    response: Response,
    keys: Sequence[str],
    *,
    ensure_success: EnsureSuccess | None = ...,
    deep: bool = ...,
) -> tuple[Any, ...]: ...


def extract_payload(
    response: Response,
    keys: str | Sequence[str] | None,
    *,
    ensure_success: EnsureSuccess | None = ensure_biz_code_success,
    deep: bool = True,
) -> Any | tuple[Any, ...] | None:
    """Extract selected values from an HTTP response JSON payload.

    This function only handles business payload parsing and validation. HTTP-layer status validation
    should be handled by `AsyncHttpClient` or its exception middleware before this function is called.

    Args:
        response: HTTP response object.
        keys: Key or keys to extract from the JSON payload.
            - If None, only validation is performed and None is returned.
            - If a string is provided, a single value is returned.
            - If a sequence of strings is provided, a tuple of values is returned in the same order.
        ensure_success: Optional payload success validator. Pass None to skip business-level validation.
        deep: Whether to support dotted paths such as `"data.items"`.

    Returns:
        None when `keys` is None, a single value when `keys` is a string, a tuple of values when `keys` is a sequence.

    Raises:
        InvalidPayloadError: If `response.json()` does not return a dict.
        PayloadBizStatusError: If business-level validation fails.
    """
    try:
        payload = response.json()
    except ValueError as exc:
        raise InvalidPayloadError("Response body is not valid JSON") from exc

    if not isinstance(payload, dict):
        raise InvalidPayloadError(
            f"response.json() should return dict, got {type(payload).__name__}.",
        )

    if ensure_success is not None:
        ensure_success(payload)

    if keys is None:
        return None

    getter = _get_by_path if deep else lambda p, k: p.get(k)

    if isinstance(keys, str):
        return getter(payload, keys)

    return tuple(getter(payload, key) for key in keys)


def _get_by_path(payload: Payload, path: str, default: Any = None) -> Any:
    """Get a value from a nested dict payload by dotted path."""
    current: Any = payload

    for part in path.split("."):
        if not isinstance(current, dict):
            return default

        current = current.get(part, _MISSING)
        if current is _MISSING:
            return default

    return current
