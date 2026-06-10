import asyncio
import json
from datetime import datetime, timedelta
from typing import Any

import pytest

import httpx
from athena_kit.http import AsyncHttpClient
from athena_kit.http.hooks import RequestIDOptions
from athena_kit.http.response_json import ResponseJSONValidationError
from athena_kit.lark import AsyncLarkClient, LarkTenantAccessTokenAuth
from athena_kit.lark.sheets import (
    SHEETS_SUCCESS_VALIDATOR,
    LarkSheetBackend,
    LarkSheetLocator,
    LarkSheetsAsyncClient,
)
from athena_kit.lark.sheets.aclient import _ensure_title
from athena_kit.lark.sheets.models import SheetWritePayload
from athena_kit.lark.sheets.range import calculate_range, col_to_index, index_to_col


def _request_json(request: httpx.Request) -> dict[str, Any]:
    return json.loads(request.content.decode())


def test_public_exports_are_lazy_loaded() -> None:
    assert AsyncLarkClient.__name__ == "AsyncLarkClient"
    assert LarkTenantAccessTokenAuth.__name__ == "LarkTenantAccessTokenAuth"
    assert LarkSheetsAsyncClient.__name__ == "LarkSheetsAsyncClient"
    assert LarkSheetBackend.__name__ == "LarkSheetBackend"


def test_sheets_success_validator_accepts_zero_code() -> None:
    SHEETS_SUCCESS_VALIDATOR({"code": 0, "msg": "ok"})


def test_sheets_success_validator_rejects_nonzero_code() -> None:
    with pytest.raises(ResponseJSONValidationError):
        SHEETS_SUCCESS_VALIDATOR({"code": 999, "msg": "failed"})


def test__ensure_title_uses_existing_title() -> None:
    assert _ensure_title(" title-1 ") == "title-1"


def test__ensure_title_uses_date_and_uuid_prefix() -> None:
    title = _ensure_title(None)

    assert len(title) == 17
    assert title[8] == "_"
    datetime.strptime(title[:8], "%Y%m%d")
    assert title[9:].isalnum()


def test_async_lark_client_uses_athena_http_hooks(monkeypatch: pytest.MonkeyPatch) -> None:
    requests: list[httpx.Request] = []

    async def get_tenant_access_token(self: LarkTenantAccessTokenAuth) -> str:
        return "token-1"

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            request=request,
            json={
                "code": 0,
                "data": {"spreadsheet": {"spreadsheet_token": "spreadsheet-1", "url": "https://sheet.test"}},
            },
        )

    monkeypatch.setattr(LarkTenantAccessTokenAuth, "get_tenant_access_token", get_tenant_access_token)

    async def run() -> None:
        async with AsyncLarkClient(
            "app_id",
            "app_secret",
            request_id=RequestIDOptions(id_factory=lambda: "request-1"),
            response_status=True,
            transport=httpx.MockTransport(handler),
        ) as client:
            await client.sheets.create_spreadsheet("folder-1", "title-1")

    asyncio.run(run())

    assert requests[0].headers["Authorization"] == "Bearer token-1"
    assert requests[0].headers["X-Request-ID"] == "request-1"


def test_async_lark_client_can_raise_for_http_status(monkeypatch: pytest.MonkeyPatch) -> None:
    async def get_tenant_access_token(self: LarkTenantAccessTokenAuth) -> str:
        return "token-1"

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, request=request, json={"code": 999, "msg": "failed"})

    monkeypatch.setattr(LarkTenantAccessTokenAuth, "get_tenant_access_token", get_tenant_access_token)

    async def run() -> None:
        async with AsyncLarkClient(
            "app_id",
            "app_secret",
            response_status=True,
            transport=httpx.MockTransport(handler),
        ) as client:
            await client.sheets.create_spreadsheet("folder-1", "title-1")

    with pytest.raises(httpx.HTTPStatusError):
        asyncio.run(run())


def test_async_lark_client_rejects_auth_kwargs() -> None:
    with pytest.raises(ValueError, match="manages auth automatically"):
        AsyncLarkClient("app_id", "app_secret", auth=LarkTenantAccessTokenAuth("app_id", "app_secret"))


def test_async_lark_client_can_be_closed_explicitly(monkeypatch: pytest.MonkeyPatch) -> None:
    for env_name in ("ALL_PROXY", "all_proxy", "HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
        monkeypatch.delenv(env_name, raising=False)

    async def run() -> AsyncLarkClient:
        client = AsyncLarkClient("app_id", "app_secret")
        await client.aclose()
        return client

    client = asyncio.run(run())

    assert client._aclient.is_closed


@pytest.mark.parametrize(
    ("col", "index"),
    [
        ("A", 1),
        ("Z", 26),
        ("AA", 27),
        ("AZ", 52),
        ("BA", 53),
    ],
)
def test_col_index_roundtrip(col: str, index: int) -> None:
    assert col_to_index(col) == index
    assert index_to_col(index) == col


def test_calculate_range() -> None:
    assert calculate_range("sheet1", n_rows=5, n_cols=4) == "sheet1!A1:D5"
    assert calculate_range("sheet1", n_rows=2, n_cols=2, start_row=3, start_col=27) == "sheet1!AA3:AB4"


def test_sheet_write_payload_encodes_values_and_validates_width() -> None:
    payload = SheetWritePayload.from_rows_values(
        headers=["name", "tags"],
        rows_values=[[" alpha ", ["x", "y"]]],
    )

    assert payload.shape() == (2, 2)
    assert payload.to_table_2dvalues() == [["name", "tags"], ["alpha", "x, y"]]

    with pytest.raises(ValueError):
        SheetWritePayload.from_rows_values(headers=["name"], rows_values=[["alpha", "extra"]])


def test_lark_auth_caches_tenant_access_token() -> None:
    class StubAuth(LarkTenantAccessTokenAuth):
        def __init__(self):
            super().__init__("app_id", "app_secret")
            self.fetch_count = 0

        async def _fetch_tenant_access_token(self) -> tuple[str, datetime]:
            self.fetch_count += 1
            return "token-1", datetime.now() + timedelta(minutes=10)

    async def run() -> None:
        auth = StubAuth()
        assert await auth.get_tenant_access_token() == "token-1"
        assert await auth.get_tenant_access_token() == "token-1"
        assert auth.fetch_count == 1

    asyncio.run(run())


def test_lark_auth_injects_headers() -> None:
    class StubAuth(LarkTenantAccessTokenAuth):
        async def _fetch_tenant_access_token(self) -> tuple[str, datetime]:
            return "token-1", datetime.now() + timedelta(minutes=10)

    seen_request: httpx.Request | None = None

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_request
        seen_request = request
        return httpx.Response(200, request=request, json={"code": 0})

    async def run() -> None:
        async with AsyncHttpClient(
            base_url="https://example.test",
            auth=StubAuth("app_id", "app_secret"),
            transport=httpx.MockTransport(handler),
        ) as client:
            await client.get("/items")

    asyncio.run(run())

    assert seen_request is not None
    assert seen_request.headers["Authorization"] == "Bearer token-1"
    assert seen_request.headers["Content-Type"] == "application/json;charset=utf-8"


def test_lark_sheets_client_create_and_add_sheet_requests() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/sheets/v3/spreadsheets":
            return httpx.Response(
                200,
                request=request,
                json={
                    "code": 0,
                    "data": {"spreadsheet": {"spreadsheet_token": "spreadsheet-1", "url": "https://sheet.test"}},
                },
            )
        return httpx.Response(
            200,
            request=request,
            json={"code": 0, "data": {"replies": [{"addSheet": {"properties": {"sheetId": "sheet-1"}}}]}},
        )

    async def run() -> tuple[tuple[str, str], str]:
        async with AsyncHttpClient(base_url="https://example.test", transport=httpx.MockTransport(handler)) as aclient:
            client = LarkSheetsAsyncClient(aclient)
            spreadsheet = await client.create_spreadsheet("folder-1", "title-1")
            sheet_id = await client.add_sheet("spreadsheet-1", "Sheet 1", 1)
            return spreadsheet, sheet_id

    spreadsheet, sheet_id = asyncio.run(run())

    assert spreadsheet == ("spreadsheet-1", "https://sheet.test")
    assert sheet_id == "sheet-1"
    assert requests[0].method == "POST"
    assert _request_json(requests[0]) == {"folder_token": "folder-1", "title": "title-1"}
    assert requests[1].url.path == "/sheets/v2/spreadsheets/spreadsheet-1/sheets_batch_update"
    assert _request_json(requests[1]) == {
        "requests": [{"addSheet": {"properties": {"title": "Sheet 1", "index": 1}}}]
    }


def test_lark_sheets_client_uses_default_titles(monkeypatch: pytest.MonkeyPatch) -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/sheets/v3/spreadsheets":
            return httpx.Response(
                200,
                request=request,
                json={
                    "code": 0,
                    "data": {"spreadsheet": {"spreadsheet_token": "spreadsheet-1", "url": "https://sheet.test"}},
                },
            )
        return httpx.Response(
            200,
            request=request,
            json={"code": 0, "data": {"replies": [{"addSheet": {"properties": {"sheetId": "sheet-1"}}}]}},
        )

    monkeypatch.setattr("athena_kit.lark.sheets.aclient._ensure_title", lambda title: "20260611_abc12345")

    async def run() -> None:
        async with AsyncHttpClient(base_url="https://example.test", transport=httpx.MockTransport(handler)) as aclient:
            client = LarkSheetsAsyncClient(aclient)
            await client.create_spreadsheet("folder-1")
            await client.add_sheet("spreadsheet-1")

    asyncio.run(run())

    assert _request_json(requests[0]) == {"folder_token": "folder-1", "title": "20260611_abc12345"}
    assert _request_json(requests[1]) == {
        "requests": [{"addSheet": {"properties": {"title": "20260611_abc12345", "index": 0}}}]
    }


def test_lark_sheets_client_overwrite_values() -> None:
    seen_payloads: list[dict[str, Any]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen_payloads.append(_request_json(request))
        return httpx.Response(200, request=request, json={"code": 0, "data": {"revision": 7, "updatedRows": 2}})

    async def run() -> tuple[int, int, int]:
        async with AsyncHttpClient(base_url="https://example.test", transport=httpx.MockTransport(handler)) as aclient:
            return await LarkSheetsAsyncClient(aclient).overwrite_values(
                "spreadsheet-1",
                "sheet-1",
                value_headers=["name", "value"],
                rows_values=[["alpha", 1]],
            )

    result = asyncio.run(run())

    assert result == (7, 2, 2)
    assert seen_payloads == [
        {"valueRange": {"range": "sheet-1!A1:B2", "values": [["name", "value"], ["alpha", 1]]}}
    ]


def test_lark_sheets_client_query_values() -> None:
    requested_paths: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requested_paths.append(request.url.path)
        if "A1:CV1" in request.url.path:
            values = [["name", "value", None, "ignored"]]
        elif "A2:B1001" in request.url.path:
            values = [["alpha", 1], [None, None]]
        else:
            values = []
        return httpx.Response(200, request=request, json={"code": 0, "data": {"valueRange": {"values": values}}})

    async def run() -> tuple[list[str], list[list[Any]]]:
        async with AsyncHttpClient(base_url="https://example.test", transport=httpx.MockTransport(handler)) as aclient:
            return await LarkSheetsAsyncClient(aclient).query_values("spreadsheet-1", "sheet-1")

    headers, rows = asyncio.run(run())

    assert headers == ["name", "value"]
    assert rows == [["alpha", 1]]
    assert requested_paths == [
        "/sheets/v2/spreadsheets/spreadsheet-1/values/sheet-1!A1:CV1",
        "/sheets/v2/spreadsheets/spreadsheet-1/values/sheet-1!A2:B1001",
        "/sheets/v2/spreadsheets/spreadsheet-1/values/sheet-1!A1002:B2001",
    ]


def test_lark_sheet_backend_requires_lark_locator() -> None:
    backend = LarkSheetBackend(LarkSheetsAsyncClient(AsyncHttpClient(base_url="https://example.test")))

    with pytest.raises(TypeError):
        backend._ensure_lark_locator(object())

    assert backend._ensure_lark_locator(LarkSheetLocator("spreadsheet-1", "sheet-1")) == LarkSheetLocator(
        "spreadsheet-1",
        "sheet-1",
    )
