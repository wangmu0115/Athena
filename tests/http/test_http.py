import asyncio

import httpx
import pytest

from athena_kit.http import AsyncHttpClient, extract_payload
from athena_kit.http.exceptions import PayloadBizStatusError
from athena_kit.http.middleware_config import RequestIDOptions
from athena_kit.http.middlewares.retry import RetryMiddleware


def test_public_exports_are_lazy_loaded() -> None:
    from athena_kit.http import Extensions, HttpClientError, LoggingOptions

    assert Extensions.__name__ == "Extensions"
    assert HttpClientError.__name__ == "HttpClientError"
    assert LoggingOptions.__name__ == "LoggingOptions"


def test_extract_payload_reads_nested_values() -> None:
    response = httpx.Response(200, json={"code": 0, "data": {"items": [1, 2, 3]}})

    assert extract_payload(response, "data.items") == [1, 2, 3]


def test_extract_payload_raises_for_business_status() -> None:
    response = httpx.Response(200, json={"code": 500, "message": "failed"})

    with pytest.raises(PayloadBizStatusError):
        extract_payload(response, None)


def test_request_id_middleware_injects_header() -> None:
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
            request_id_options=RequestIDOptions(id_factory=lambda: "request-1"),
        ) as client:
            await client.get("/items")

    asyncio.run(run_request())

    assert seen_request is not None
    assert seen_request.headers["X-Request-ID"] == "request-1"


def test_retry_after_parser_accepts_delta_seconds() -> None:
    assert RetryMiddleware._parse_retry_after("3") == 3.0


def test_retry_after_parser_rejects_invalid_values() -> None:
    assert RetryMiddleware._parse_retry_after("not-a-date") is None
