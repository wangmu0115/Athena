from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.http.aclient import AsyncHttpClient
    from athena_kit.http.client import HttpClient
    from athena_kit.http.rate_limit import (
        AsyncCompositeRateLimiter,
        AsyncRateLimiter,
        AsyncRouteRateLimiter,
        AsyncSlidingWindowRateLimiter,
        CompositeRateLimiter,
        RateLimit,
        RateLimiter,
        RouteRateLimiter,
        SlidingWindowRateLimiter,
    )
    from athena_kit.http.response_json import (
        InvalidResponseJSONError,
        JSONArray,
        JSONObject,
        JSONObjectValidator,
        JSONPath,
        JSONScalar,
        JSONValue,
        ResponseJSONError,
        ResponseJSONValidationError,
        create_biz_code_validator,
        extract_response_json_value,
        extract_response_json_values,
        parse_response_json,
    )
    from athena_kit.http.retrying import RetryOptions, retry, retry_async

__all__ = (
    "AsyncHttpClient",
    "HttpClient",
    "AsyncCompositeRateLimiter",
    "AsyncRateLimiter",
    "AsyncRouteRateLimiter",
    "AsyncSlidingWindowRateLimiter",
    "CompositeRateLimiter",
    "RateLimit",
    "RateLimiter",
    "RouteRateLimiter",
    "SlidingWindowRateLimiter",
    "InvalidResponseJSONError",
    "JSONArray",
    "JSONObject",
    "JSONObjectValidator",
    "JSONPath",
    "JSONScalar",
    "JSONValue",
    "ResponseJSONError",
    "ResponseJSONValidationError",
    "create_biz_code_validator",
    "extract_response_json_value",
    "extract_response_json_values",
    "parse_response_json",
    "RetryOptions",
    "retry",
    "retry_async",
)

_dynamic_imports = {
    "AsyncHttpClient": "aclient",
    "HttpClient": "client",
    "AsyncCompositeRateLimiter": "rate_limit",
    "AsyncRateLimiter": "rate_limit",
    "AsyncRouteRateLimiter": "rate_limit",
    "AsyncSlidingWindowRateLimiter": "rate_limit",
    "CompositeRateLimiter": "rate_limit",
    "RateLimit": "rate_limit",
    "RateLimiter": "rate_limit",
    "RouteRateLimiter": "rate_limit",
    "SlidingWindowRateLimiter": "rate_limit",
    "InvalidResponseJSONError": "response_json",
    "JSONArray": "response_json",
    "JSONObject": "response_json",
    "JSONObjectValidator": "response_json",
    "JSONPath": "response_json",
    "JSONScalar": "response_json",
    "JSONValue": "response_json",
    "ResponseJSONError": "response_json",
    "ResponseJSONValidationError": "response_json",
    "create_biz_code_validator": "response_json",
    "extract_response_json_value": "response_json",
    "extract_response_json_values": "response_json",
    "parse_response_json": "response_json",
    "RetryOptions": "retrying",
    "retry": "retrying",
    "retry_async": "retrying",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
