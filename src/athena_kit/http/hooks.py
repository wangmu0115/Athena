import logging
import time
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

import httpx

EventHook = Callable[..., Awaitable[None]]


@dataclass(slots=True)
class RequestIDOptions:
    """Options for the request ID event hook.

    Reference:
        HTTPX Event Hooks: https://www.python-httpx.org/advanced/event-hooks/
    """

    header_name: str = "X-Request-ID"
    id_factory: Callable[[], str] = lambda: str(uuid.uuid4())


@dataclass(slots=True)
class LoggingOptions:
    """Options for request/response logging event hooks.

    Reference:
        HTTPX Event Hooks: https://www.python-httpx.org/advanced/event-hooks/
    """

    logger: logging.Logger | None = None
    level: int = logging.INFO
    log_headers: bool = False


SENSITIVE_HEADERS = frozenset({"authorization", "cookie", "set-cookie", "x-api-key"})
_START_TIME_KEY = "athena_kit.http.start_time"


def make_request_id_hook(options: RequestIDOptions | None = None) -> EventHook:
    """Create an async HTTPX request hook that injects a request ID header.

    Change note:
        This replaces the old `RequestIDMiddleware` with HTTPX's native request
        event hook mechanism.

    Reference:
        HTTPX Event Hooks: https://www.python-httpx.org/advanced/event-hooks/
    """
    resolved = options or RequestIDOptions()

    async def add_request_id(request: httpx.Request) -> None:
        request.headers.setdefault(resolved.header_name, resolved.id_factory())

    return add_request_id


def make_logging_hooks(options: LoggingOptions | None = None) -> tuple[EventHook, EventHook]:
    """Create async HTTPX request/response hooks for simple structured logging.

    Change note:
        This replaces the old `LoggingMiddleware` with HTTPX's native event hooks.
        Async clients require async hook callables.

    Reference:
        HTTPX Event Hooks: https://www.python-httpx.org/advanced/event-hooks/
    """
    resolved = options or LoggingOptions()
    logger = resolved.logger or logging.getLogger("athena_kit.http")

    async def log_request(request: httpx.Request) -> None:
        request.extensions[_START_TIME_KEY] = time.perf_counter()
        headers = _mask_headers(request.headers) if resolved.log_headers else None
        logger.log(
            resolved.level,
            "HTTP request started: method=%s url=%s headers=%s",
            request.method,
            request.url,
            headers,
        )

    async def log_response(response: httpx.Response) -> None:
        start_time = response.request.extensions.get(_START_TIME_KEY)
        elapsed_ms = None
        if isinstance(start_time, float):
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        logger.log(
            resolved.level,
            "HTTP request completed: method=%s url=%s status_code=%s elapsed_ms=%s",
            response.request.method,
            response.request.url,
            response.status_code,
            None if elapsed_ms is None else round(elapsed_ms, 2),
        )

    return log_request, log_response


async def raise_for_status_hook(response: httpx.Response) -> None:
    """Raise `httpx.HTTPStatusError` for non-2xx responses.

    Change note:
        This replaces the old `HttpExceptionMiddleware` with a response event
        hook that delegates to HTTPX's native `Response.raise_for_status()`.

    Reference:
        HTTPX Event Hooks: https://www.python-httpx.org/advanced/event-hooks/
        HTTPX Exceptions: https://www.python-httpx.org/exceptions/
    """
    response.raise_for_status()


def merge_event_hooks(
    event_hooks: dict[str, list[EventHook]] | None = None,
    *,
    request_id: RequestIDOptions | None = None,
    logging_options: LoggingOptions | None = None,
    raise_for_status: bool = False,
) -> dict[str, list[EventHook]]:
    """Merge Athena's optional hooks with caller-provided HTTPX hooks."""
    request_hooks = list((event_hooks or {}).get("request", []))
    response_hooks = list((event_hooks or {}).get("response", []))

    if request_id is not None:
        request_hooks.append(make_request_id_hook(request_id))

    if logging_options is not None:
        log_request, log_response = make_logging_hooks(logging_options)
        request_hooks.append(log_request)
        response_hooks.append(log_response)

    if raise_for_status:
        response_hooks.append(raise_for_status_hook)

    return {
        "request": request_hooks,
        "response": response_hooks,
    }


def _mask_headers(headers: httpx.Headers) -> dict[str, str]:
    return {key: "******" if key.lower() in SENSITIVE_HEADERS else value for key, value in headers.items()}
