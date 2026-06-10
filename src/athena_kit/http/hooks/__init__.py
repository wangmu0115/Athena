"""HTTPX event hook helpers for Athena HTTP Clients.

References:
    HTTPX Event Hooks: https://www.python-httpx.org/advanced/event-hooks/
    HTTPX Exceptions: https://www.python-httpx.org/exceptions/
"""

from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.http.hooks.event_hooks import build_async_event_hooks, build_event_hooks
    from athena_kit.http.hooks.logging import LoggingOptions, create_async_logging_hooks, create_logging_hooks
    from athena_kit.http.hooks.request_id import RequestIDOptions, create_async_request_id_hook, create_request_id_hook
    from athena_kit.http.hooks.response_status import (
        ResponseStatusOptions,
        create_async_response_status_hook,
        create_response_status_hook,
    )
    from athena_kit.http.hooks.types import (
        AsyncEventHooks,
        AsyncRequestHook,
        AsyncResponseHook,
        EventHooks,
        RequestHook,
        ResponseHook,
    )

__all__ = (
    "AsyncEventHooks",
    "AsyncRequestHook",
    "AsyncResponseHook",
    "EventHooks",
    "LoggingOptions",
    "ResponseStatusOptions",
    "RequestHook",
    "RequestIDOptions",
    "ResponseHook",
    "build_async_event_hooks",
    "build_event_hooks",
    "create_async_logging_hooks",
    "create_async_response_status_hook",
    "create_async_request_id_hook",
    "create_logging_hooks",
    "create_response_status_hook",
    "create_request_id_hook",
)

_dynamic_imports = {
    "AsyncEventHooks": "types",
    "AsyncRequestHook": "types",
    "AsyncResponseHook": "types",
    "EventHooks": "types",
    "LoggingOptions": "logging",
    "ResponseStatusOptions": "response_status",
    "RequestHook": "types",
    "RequestIDOptions": "request_id",
    "ResponseHook": "types",
    "build_async_event_hooks": "event_hooks",
    "build_event_hooks": "event_hooks",
    "create_async_logging_hooks": "logging",
    "create_async_response_status_hook": "response_status",
    "create_async_request_id_hook": "request_id",
    "create_logging_hooks": "logging",
    "create_response_status_hook": "response_status",
    "create_request_id_hook": "request_id",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
