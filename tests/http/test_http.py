import asyncio

import pytest

import httpx
from athena_kit.http import AsyncHttpClient, RequestIDOptions, extract_payload
from athena_kit.http.exceptions import PayloadBizStatusError
from athena_kit.http.hooks import create_async_request_id_hook, create_request_id_hook, raise_for_status_hook


def test_public_exports_are_lazy_loaded() -> None:
    from athena_kit.http import LoggingOptions, create_logging_hooks

    assert AsyncHttpClient.__name__ == "AsyncHttpClient"
    assert LoggingOptions.__name__ == "LoggingOptions"
    assert callable(create_logging_hooks)


def test_extract_payload_reads_nested_values() -> None:
    response = httpx.Response(200, json={"code": 0, "data": {"items": [1, 2, 3]}})

    assert extract_payload(response, "data.items") == [1, 2, 3]


def test_extract_payload_raises_for_business_status() -> None:
    response = httpx.Response(200, json={"code": 500, "message": "failed"})

    with pytest.raises(PayloadBizStatusError):
        extract_payload(response, None)


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


def test_raise_for_status_hook_delegates_to_httpx() -> None:
    request = httpx.Request("GET", "https://example.test/items")
    response = httpx.Response(500, request=request)

    with pytest.raises(httpx.HTTPStatusError):
        raise_for_status_hook(response)
