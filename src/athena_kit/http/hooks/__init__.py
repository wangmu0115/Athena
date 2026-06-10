"""HTTPX event hook helpers for Athena HTTP Clients.

References:
    HTTPX Event Hooks: https://www.python-httpx.org/advanced/event-hooks/
    HTTPX Exceptions: https://www.python-httpx.org/exceptions/
"""

from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.http.hooks.logging import LoggingOptions, create_async_logging_hooks, create_logging_hooks
    from athena_kit.http.hooks.merge import merge_async_event_hooks, merge_event_hooks
    from athena_kit.http.hooks.raise_for_status import (
        RaiseForStatusOptions,
        async_raise_for_status_hook,
        create_async_raise_for_status_hook,
        create_raise_for_status_hook,
        raise_for_status_hook,
    )
    from athena_kit.http.hooks.request_id import RequestIDOptions, create_async_request_id_hook, create_request_id_hook
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
    "RaiseForStatusOptions",
    "RequestHook",
    "RequestIDOptions",
    "ResponseHook",
    "async_raise_for_status_hook",
    "create_async_logging_hooks",
    "create_async_raise_for_status_hook",
    "create_async_request_id_hook",
    "create_logging_hooks",
    "create_raise_for_status_hook",
    "create_request_id_hook",
    "merge_async_event_hooks",
    "merge_event_hooks",
    "raise_for_status_hook",
)

_dynamic_imports = {
    "AsyncEventHooks": "types",
    "AsyncRequestHook": "types",
    "AsyncResponseHook": "types",
    "EventHooks": "types",
    "LoggingOptions": "logging",
    "RaiseForStatusOptions": "raise_for_status",
    "RequestHook": "types",
    "RequestIDOptions": "request_id",
    "ResponseHook": "types",
    "create_async_logging_hooks": "logging",
    "create_async_raise_for_status_hook": "raise_for_status",
    "create_async_request_id_hook": "request_id",
    "create_logging_hooks": "logging",
    "create_raise_for_status_hook": "raise_for_status",
    "create_request_id_hook": "request_id",
    "async_raise_for_status_hook": "raise_for_status",
    "raise_for_status_hook": "raise_for_status",
    "merge_async_event_hooks": "merge",
    "merge_event_hooks": "merge",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
