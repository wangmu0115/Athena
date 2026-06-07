from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.http.aclient import AsyncHttpClient
    from athena_kit.http.exceptions import (
        InvalidPayloadError,
        PayloadBizStatusError,
        PayloadError,
    )
    from athena_kit.http.hooks import (
        AsyncEventHooks,
        AsyncRequestHook,
        AsyncResponseHook,
        EventHooks,
        LoggingOptions,
        RequestHook,
        RequestIDOptions,
        ResponseHook,
        async_raise_for_status_hook,
        create_async_logging_hooks,
        create_async_request_id_hook,
        create_logging_hooks,
        create_request_id_hook,
        merge_async_event_hooks,
        merge_event_hooks,
        raise_for_status_hook,
    )
    from athena_kit.http.payload import (
        ensure_biz_code_success,
        extract_payload,
        make_biz_code_validator,
    )

__all__ = (
    "AsyncHttpClient",
    "AsyncEventHooks",
    "AsyncRequestHook",
    "AsyncResponseHook",
    "EventHooks",
    "LoggingOptions",
    "RequestHook",
    "RequestIDOptions",
    "ResponseHook",
    "PayloadError",
    "InvalidPayloadError",
    "PayloadBizStatusError",
    "create_async_request_id_hook",
    "create_request_id_hook",
    "create_async_logging_hooks",
    "create_logging_hooks",
    "async_raise_for_status_hook",
    "raise_for_status_hook",
    "merge_async_event_hooks",
    "merge_event_hooks",
    "ensure_biz_code_success",
    "extract_payload",
    "make_biz_code_validator",
)

_dynamic_imports = {
    "AsyncHttpClient": "aclient",
    "AsyncEventHooks": "hooks",
    "AsyncRequestHook": "hooks",
    "AsyncResponseHook": "hooks",
    "EventHooks": "hooks",
    "LoggingOptions": "hooks",
    "RequestHook": "hooks",
    "RequestIDOptions": "hooks",
    "ResponseHook": "hooks",
    "create_async_logging_hooks": "hooks",
    "create_async_request_id_hook": "hooks",
    "create_logging_hooks": "hooks",
    "create_request_id_hook": "hooks",
    "async_raise_for_status_hook": "hooks",
    "raise_for_status_hook": "hooks",
    "merge_async_event_hooks": "hooks",
    "merge_event_hooks": "hooks",
    "PayloadError": "exceptions",
    "InvalidPayloadError": "exceptions",
    "PayloadBizStatusError": "exceptions",
    "ensure_biz_code_success": "payload",
    "extract_payload": "payload",
    "make_biz_code_validator": "payload",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
