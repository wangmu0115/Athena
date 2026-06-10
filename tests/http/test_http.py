import asyncio
import logging

import pytest

import httpx
from athena_kit.http import (
    AsyncHttpClient,
    HttpClient,
    RetryOptions,
    create_biz_code_validator,
    extract_response_json_value,
    extract_response_json_values,
    retry,
    retry_async,
)
from athena_kit.http.hooks import (
    LoggingOptions,
    RequestIDOptions,
    ResponseStatusOptions,
    create_async_request_id_hook,
    create_logging_hooks,
    create_request_id_hook,
    create_response_status_hook,
)
from athena_kit.http.response_json import ResponseJSONValidationError


def test_public_exports_are_lazy_loaded() -> None:
    assert AsyncHttpClient.__name__ == "AsyncHttpClient"
    assert HttpClient.__name__ == "HttpClient"
    assert LoggingOptions.__name__ == "LoggingOptions"
    assert callable(create_logging_hooks)


def test_extract_response_json_value_reads_convenience_path() -> None:
    response = httpx.Response(200, json={"code": 0, "data": {"items": [1, 2, 3]}})
    validator = create_biz_code_validator()

    assert extract_response_json_value(response, "data.items", validator=validator) == [1, 2, 3]


def test_extract_response_json_value_raises_for_business_status() -> None:
    response = httpx.Response(200, json={"code": 500, "message": "failed"})
    validator = create_biz_code_validator()

    with pytest.raises(ResponseJSONValidationError):
        extract_response_json_value(response, validator=validator)


def test_extract_response_json_value_reads_explicit_path_for_literal_dotted_field() -> None:
    response = httpx.Response(200, json={"code": 0, "data.items": {"value": [1, 2, 3]}})
    validator = create_biz_code_validator()

    assert extract_response_json_value(response, ["data.items", "value"], validator=validator) == [
        1,
        2,
        3,
    ]


@pytest.mark.parametrize("path", ["", [], ["data", ""], "data..items", "data.items[x]"])
def test_extract_response_json_value_rejects_invalid_path(path: object) -> None:
    response = httpx.Response(200, json={"code": 0, "data": {"items": [1, 2, 3]}})

    with pytest.raises(ValueError):
        extract_response_json_value(response, path)  # type: ignore[arg-type]


def test_extract_response_json_value_reads_array_path() -> None:
    response = httpx.Response(200, json=[{"name": "alpha"}, {"name": "beta"}])

    assert extract_response_json_value(response, [1, "name"]) == "beta"


def test_extract_response_json_value_distinguishes_object_keys_and_array_indexes() -> None:
    object_response = httpx.Response(200, json={"0": "hello"})
    array_response = httpx.Response(200, json=["hello"])

    assert extract_response_json_value(object_response, "0") == "hello"
    assert extract_response_json_value(object_response, 0) is None
    assert extract_response_json_value(array_response, 0) == "hello"
    assert extract_response_json_value(array_response, [0]) == "hello"


@pytest.mark.parametrize("path", ["[0]", "abc0]", "abc[0", "abc[0][1]"])
def test_extract_response_json_value_rejects_invalid_convenience_path_segments(path: str) -> None:
    response = httpx.Response(200, json={"abc": ["hello"]})

    with pytest.raises(ValueError):
        extract_response_json_value(response, path)


def test_extract_response_json_value_returns_scalar_values() -> None:
    response = httpx.Response(200, json="ok")

    assert extract_response_json_value(response) == "ok"


def test_extract_response_json_values_reads_multiple_paths_with_one_validation() -> None:
    response = httpx.Response(200, json={"code": 0, "data": {"items": [{"id": 1}]}, "total": 1})
    validator = create_biz_code_validator()

    assert extract_response_json_values(
        response,
        ["data.items[0].id", "total"],
        validator=validator,
    ) == (1, 1)


def test_extract_response_json_values_returns_none_for_missing_paths() -> None:
    response = httpx.Response(200, json={"data": {"items": [{"id": 1}]}})

    assert extract_response_json_values(response, ["data.items[0].id", "data.total"]) == (1, None)


def test_request_id_hook_injects_header() -> None:
    request = httpx.Request("GET", "https://example.test/items")
    hook = create_request_id_hook(RequestIDOptions(id_factory=lambda: "request-1"))

    hook(request)

    assert request.headers["X-Request-ID"] == "request-1"


def test_async_request_id_hook_injects_header() -> None:
    async def run_hook() -> httpx.Request:
        request = httpx.Request("GET", "https://example.test/items")
        hook = create_async_request_id_hook(RequestIDOptions(id_factory=lambda: "request-1"))
        await hook(request)
        return request

    request = asyncio.run(run_hook())

    assert request.headers["X-Request-ID"] == "request-1"


def test_async_http_client_uses_httpx_event_hooks() -> None:
    seen_request: httpx.Request | None = None

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_request
        seen_request = request
        return httpx.Response(200, request=request, json={"code": 0})

    transport = httpx.MockTransport(handler)

    async def run_request() -> None:
        async with AsyncHttpClient(
            base_url="https://example.test",
            transport=transport,
            request_id=RequestIDOptions(id_factory=lambda: "request-2"),
        ) as client:
            await client.get("/items")

    asyncio.run(run_request())

    assert seen_request is not None
    assert seen_request.headers["X-Request-ID"] == "request-2"


def test_http_client_uses_httpx_event_hooks() -> None:
    seen_request: httpx.Request | None = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_request
        seen_request = request
        return httpx.Response(200, request=request, json={"code": 0})

    transport = httpx.MockTransport(handler)

    with HttpClient(
        base_url="https://example.test",
        transport=transport,
        request_id=RequestIDOptions(id_factory=lambda: "request-3"),
    ) as client:
        client.get("/items")

    assert seen_request is not None
    assert seen_request.headers["X-Request-ID"] == "request-3"


def test_retry_retries_by_result() -> None:
    attempts = 0

    def request() -> int:
        nonlocal attempts
        attempts += 1
        return attempts

    result = retry(
        request,
        options=RetryOptions(attempts=3, initial_delay=0),
        should_retry_result=lambda value: value < 3,
    )

    assert result == 3
    assert attempts == 3


def test_retry_retries_by_exception() -> None:
    attempts = 0

    def request() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise httpx.TimeoutException("timeout")
        return "ok"

    result = retry(request, options=RetryOptions(attempts=2, initial_delay=0))

    assert result == "ok"
    assert attempts == 2


def test_retry_async_retries_by_result() -> None:
    attempts = 0

    async def request() -> int:
        nonlocal attempts
        attempts += 1
        return attempts

    async def run_retry() -> int:
        return await retry_async(
            request,
            options=RetryOptions(attempts=3, initial_delay=0),
            should_retry_result=lambda value: value < 3,
        )

    result = asyncio.run(run_retry())

    assert result == 3
    assert attempts == 3


def test_retry_logs_before_retry(caplog: pytest.LogCaptureFixture) -> None:
    attempts = 0

    def request() -> int:
        nonlocal attempts
        attempts += 1
        return attempts

    with caplog.at_level(logging.WARNING, logger="athena_kit.http.retry"):
        result = retry(
            request,
            options=RetryOptions(attempts=2, initial_delay=0, jitter=0, logger=True),
            should_retry_result=lambda value: value < 2,
        )

    assert result == 2
    assert "Retrying HTTP request" in caplog.text
    assert "retry=1/1" in caplog.text
    assert "reason=result" in caplog.text


def test_response_status_hook_delegates_to_httpx() -> None:
    request = httpx.Request("GET", "https://example.test/items")
    response = httpx.Response(500, request=request)
    hook = create_response_status_hook()

    with pytest.raises(httpx.HTTPStatusError):
        hook(response)


def test_response_status_hook_allows_redirects_by_default() -> None:
    request = httpx.Request("GET", "https://example.test/items")
    response = httpx.Response(302, headers={"location": "https://example.test/new-items"}, request=request)
    hook = create_response_status_hook()

    hook(response)


def test_response_status_hook_can_raise_on_redirects() -> None:
    request = httpx.Request("GET", "https://example.test/items")
    response = httpx.Response(302, headers={"location": "https://example.test/new-items"}, request=request)
    hook = create_response_status_hook(ResponseStatusOptions(raise_on_redirects=True))

    with pytest.raises(httpx.HTTPStatusError):
        hook(response)


def test_response_status_hook_allows_configured_status_codes() -> None:
    request = httpx.Request("GET", "https://example.test/items")
    response = httpx.Response(404, request=request)
    hook = create_response_status_hook(ResponseStatusOptions(allowed_status_codes={404}))

    hook(response)
