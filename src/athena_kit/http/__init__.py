from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.http.client import AsyncHttpClient
    from athena_kit.http.exceptions import (
        HttpClientError,
        HttpRequestError,
        HttpResponseError,
        HttpTimeoutError,
        InvalidPayloadError,
        PayloadBizStatusError,
        PayloadError,
    )
    from athena_kit.http.middleware_config import (
        Extensions,
        LoggingOptions,
        RequestContext,
        RequestIDOptions,
        RetryOptions,
    )
    from athena_kit.http.payload import (
        ensure_biz_code_success,
        extract_payload,
        make_biz_code_validator,
    )
    from athena_kit.http.types import (
        Middleware,
        RequestHandler,
        get_middleware_name,
    )

__all__ = (
    "AsyncHttpClient",
    "Extensions",
    "LoggingOptions",
    "RequestContext",
    "RequestIDOptions",
    "RetryOptions",
    "Middleware",
    "get_middleware_name",
    "RequestHandler",
    "HttpClientError",
    "HttpRequestError",
    "HttpResponseError",
    "HttpTimeoutError",
    "PayloadError",
    "InvalidPayloadError",
    "PayloadBizStatusError",
    "ensure_biz_code_success",
    "extract_payload",
    "make_biz_code_validator",
)

_dynamic_imports = {
    "AsyncHttpClient": "client",
    "Extensions": "middleware_config",
    "LoggingOptions": "middleware_config",
    "RequestContext": "middleware_config",
    "RequestIDOptions": "middleware_config",
    "RetryOptions": "middleware_config",
    "RequestHandler": "types",
    "Middleware": "types",
    "get_middleware_name": "types",
    "HttpClientError": "exceptions",
    "HttpRequestError": "exceptions",
    "HttpResponseError": "exceptions",
    "HttpTimeoutError": "exceptions",
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
