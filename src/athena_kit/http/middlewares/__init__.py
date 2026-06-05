"""HTTP middleware package.

This package contains reusable HTTP middlewares for AsyncHttpClient.

Middleware contract:
    A middleware must satisfy the following protocol: `Callable[[RequestHandler], RequestHandler]`

Supported implementation styles:
    1. Factory function
        Use this style for simple, stateless, or lightly configurable middlewares.
        Example: `request_id_middleware`

    2. Callable class
        Use this style for complex middlewares that contain richer strategy, configuration, or internal helper methods.
        Example: `RetryMiddleware`

Design rules:
    - Implementation style may vary.
    - Public middleware contract must remain consistent.
    - Middleware should focus on one cross-cutting concern.
    - Middleware should not parse business payloads.
    - Middleware should not depend on integration or domain logic.
    - Middlewares declared later are closer to the transport layer.
      A middleware that needs raw responses should be declared after the exception-normalization middleware.

Default response order:
    _do_request -> RetryMiddleware -> http_exception_middleware -> LoggingMiddleware -> request_id_middleware
"""

from athena_kit._import_utils import import_attr
from athena_kit.http.middlewares.http_exception import http_exception_middleware
from athena_kit.http.middlewares.logging import LoggingMiddleware
from athena_kit.http.middlewares.request_id import request_id_middleware
from athena_kit.http.middlewares.retry import RetryMiddleware

DEFAULT_MIDDLEWARES = [
    request_id_middleware(),
    LoggingMiddleware(),
    http_exception_middleware(),
    RetryMiddleware(),
]

__all__ = (
    "DEFAULT_MIDDLEWARES",
    "request_id_middleware",
    "LoggingMiddleware",
    "http_exception_middleware",
    "RetryMiddleware",
)

_dynamic_imports = {
    "request_id_middleware": "request_id",
    "LoggingMiddleware": "logging",
    "http_exception_middleware": "http_exception",
    "RetryMiddleware": "retry",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
