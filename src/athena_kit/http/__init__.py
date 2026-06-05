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
        LoggingOptions,
        RequestIDOptions,
        make_logging_hooks,
        make_request_id_hook,
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
    "LoggingOptions",
    "RequestIDOptions",
    "PayloadError",
    "InvalidPayloadError",
    "PayloadBizStatusError",
    "make_request_id_hook",
    "make_logging_hooks",
    "raise_for_status_hook",
    "merge_event_hooks",
    "ensure_biz_code_success",
    "extract_payload",
    "make_biz_code_validator",
)

_dynamic_imports = {
    "AsyncHttpClient": "aclient",
    "LoggingOptions": "hooks",
    "RequestIDOptions": "hooks",
    "make_request_id_hook": "hooks",
    "make_logging_hooks": "hooks",
    "raise_for_status_hook": "hooks",
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
