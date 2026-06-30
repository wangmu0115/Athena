import asyncio
import json
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from pydantic import ValidationError

import httpx
from athena_kit.http import AsyncHttpClient
from athena_kit.http.hooks import RequestIDOptions
from athena_kit.lark import AsyncLarkClient, LarkTenantAccessTokenAuth
from athena_kit.lark.bitables import (
    BitableFieldType,
    BitableFieldUiType,
    LarkBitableFieldsAsyncClient,
    LarkBitablesAsyncClient,
)
from athena_kit.lark.sheets import (
    AsyncLarkSheetsBackend,
    LarkSheetsAsyncClient,
)
from athena_kit.lark.sheets.a1_notation import build_a1_range, column_index_to_name, column_name_to_index
from athena_kit.lark.sheets.aclient import _ensure_title
from athena_kit.lark.sheets.requests import SheetWritePayload


def _request_json(request: httpx.Request) -> dict[str, Any]:
    return json.loads(request.content.decode())


def test_public_exports_are_lazy_loaded() -> None:
    assert AsyncLarkClient.__name__ == "AsyncLarkClient"
    assert LarkTenantAccessTokenAuth.__name__ == "LarkTenantAccessTokenAuth"
    assert LarkSheetsAsyncClient.__name__ == "LarkSheetsAsyncClient"
    assert AsyncLarkSheetsBackend.__name__ == "AsyncLarkSheetsBackend"
    assert LarkBitablesAsyncClient.__name__ == "LarkBitablesAsyncClient"
    assert LarkBitableFieldsAsyncClient.__name__ == "LarkBitableFieldsAsyncClient"
    assert BitableFieldType.TEXT == 1
    assert BitableFieldType.TEXT.label == "文本"
    assert BitableFieldType.STAGE == 24
    assert BitableFieldType.BUTTON == 3001
    assert BitableFieldUiType.EMAIL == "Email"
    assert BitableFieldUiType.EMAIL.label == "邮箱"


def test_lark_bitables_client_search_records_paginates() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.params.get("page_token") is None:
            data = {
                "has_more": True,
                "page_token": "page-2",
                "items": [{"record_id": "rec-1", "fields": {"name": "alpha"}}],
            }
        else:
            data = {
                "has_more": False,
                "page_token": "",
                "items": [{"record_id": "rec-2", "fields": {"name": "beta"}}],
            }
        return httpx.Response(200, request=request, json={"code": 0, "data": data})

    async def run() -> list[dict[str, Any]]:
        async with AsyncHttpClient(base_url="https://example.test", transport=httpx.MockTransport(handler)) as aclient:
            return await LarkBitablesAsyncClient(aclient).records.get_table_records(
                "app-1",
                "table-1",
                view_id="view-1",
                field_names=["name"],
                page_size=100,
            )

    records = asyncio.run(run())

    assert records == [
        {"record_id": "rec-1", "fields": {"name": "alpha"}},
        {"record_id": "rec-2", "fields": {"name": "beta"}},
    ]
    assert [request.url.path for request in requests] == [
        "/bitable/v1/apps/app-1/tables/table-1/records/search",
        "/bitable/v1/apps/app-1/tables/table-1/records/search",
    ]
    assert [request.url.params["page_size"] for request in requests] == ["100", "100"]
    assert requests[1].url.params["page_token"] == "page-2"
    assert _request_json(requests[0]) == {
        "view_id": "view-1",
        "field_names": ["name"],
    }
    assert "page_token" not in _request_json(requests[1])


def test_lark_bitables_client_get_table_records_can_include_metadata() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            request=request,
            json={
                "code": 0,
                "data": {
                    "has_more": False,
                    "page_token": "",
                    "items": [
                        {
                            "record_id": "rec-1",
                            "fields": {"name": "alpha"},
                            "created_by": {"id": "ou-1", "name": "Alice"},
                            "created_time": 1691049973000,
                            "last_modified_by": {"id": "ou-2", "name": "Bob"},
                            "last_modified_time": 1702455191000,
                        }
                    ],
                },
            },
        )

    async def run() -> list[dict[str, Any]]:
        async with AsyncHttpClient(base_url="https://example.test", transport=httpx.MockTransport(handler)) as aclient:
            return await LarkBitablesAsyncClient(aclient).records.get_table_records(
                "app-1",
                "table-1",
                include_metadata=True,
            )

    records = asyncio.run(run())

    assert _request_json(requests[0]) == {"automatic_fields": True}
    assert records == [
        {
            "record_id": "rec-1",
            "fields": {"name": "alpha"},
            "created_by": {"id": "ou-1", "name": "Alice"},
            "created_time": datetime(2023, 8, 3, 8, 6, 13, tzinfo=UTC),
            "last_modified_by": {"id": "ou-2", "name": "Bob"},
            "last_modified_time": datetime(2023, 12, 13, 8, 13, 11, tzinfo=UTC),
        }
    ]


def test_lark_bitables_client_search_records_honors_limit() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            request=request,
            json={
                "code": 0,
                "data": {
                    "has_more": True,
                    "page_token": "page-2",
                    "items": [
                        {"record_id": "rec-1", "fields": {}},
                        {"record_id": "rec-2", "fields": {}},
                    ],
                },
            },
        )

    async def run() -> list[dict[str, Any]]:
        async with AsyncHttpClient(base_url="https://example.test", transport=httpx.MockTransport(handler)) as aclient:
            return await LarkBitablesAsyncClient(aclient).records.get_table_records("app-1", "table-1", limit=1)

    records = asyncio.run(run())

    assert records == [{"record_id": "rec-1", "fields": {}}]
    assert len(requests) == 1
    assert requests[0].url.params["page_size"] == "200"


def test_lark_bitables_client_search_records_validates_limit() -> None:
    async def run() -> None:
        async with AsyncHttpClient(base_url="https://example.test") as aclient:
            records = LarkBitablesAsyncClient(aclient).records
            assert await records.get_table_records("app-1", "table-1", limit=0) == []
            await records.get_table_records("app-1", "table-1", limit=-1)

    with pytest.raises(ValueError, match="limit"):
        asyncio.run(run())


def test_lark_bitables_fields_client_gets_table_fields() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.params.get("page_token") is None:
            data = {
                "has_more": True,
                "page_token": "page-2",
                "items": [
                    {
                        "field_id": "fld-1",
                        "field_name": "Name",
                        "type": 1,
                        "property": None,
                        "is_primary": True,
                        "ui_type": "Text",
                    }
                ],
            }
        else:
            data = {
                "has_more": False,
                "page_token": "",
                "items": [
                    {
                        "field_id": "fld-2",
                        "field_name": "Status",
                        "type": 3,
                        "property": {"options": []},
                        "ui_type": "SingleSelect",
                    }
                ],
            }
        return httpx.Response(200, request=request, json={"code": 0, "data": data})

    async def run() -> list[dict[str, Any]]:
        async with AsyncHttpClient(base_url="https://example.test", transport=httpx.MockTransport(handler)) as aclient:
            return await LarkBitableFieldsAsyncClient(aclient).get_table_fields(
                "app-1",
                "table-1",
                view_id="view-1",
            )

    fields = asyncio.run(run())

    assert fields == [
        {
            "field_id": "fld-1",
            "field_name": "Name",
            "type": BitableFieldType.TEXT,
            "property": None,
            "is_primary": True,
            "is_hidden": False,
            "ui_type": BitableFieldUiType.TEXT,
        },
        {
            "field_id": "fld-2",
            "field_name": "Status",
            "type": BitableFieldType.SINGLE_SELECT,
            "property": {"options": []},
            "is_primary": False,
            "is_hidden": False,
            "ui_type": BitableFieldUiType.SINGLE_SELECT,
        },
    ]
    assert [request.url.path for request in requests] == [
        "/bitable/v1/apps/app-1/tables/table-1/fields",
        "/bitable/v1/apps/app-1/tables/table-1/fields",
    ]
    assert str(requests[0].url.params) == "page_size=50&view_id=view-1"
    assert requests[1].url.params["page_token"] == "page-2"


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
    assert column_name_to_index(col) == index
    assert column_index_to_name(index) == col


def test_build_a1_range() -> None:
    assert build_a1_range("sheet1", n_rows=5, n_cols=4) == "sheet1!A1:D5"
    assert build_a1_range("sheet1", n_rows=2, n_cols=2, start_row=3, start_col=27) == "sheet1!AA3:AB4"


def test_sheet_write_payload_encodes_values_and_allows_rows_wider_than_headers() -> None:
    payload = SheetWritePayload.from_rows_values(
        headers=["name", "tags"],
        rows_values=[[" alpha ", ["x", "y"], "extra"]],
    )

    assert payload.shape() == (2, 3)
    assert payload.to_table_2dvalues() == [["name", "tags"], ["alpha", '["x", "y"]', "extra"]]


def test_sheet_write_payload_allows_header_only_write() -> None:
    payload = SheetWritePayload.from_rows_values(headers=["name", "value"], rows_values=[])

    assert payload.shape() == (1, 2)
    assert payload.to_table_2dvalues() == [["name", "value"]]


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
    assert _request_json(requests[1]) == {"requests": [{"addSheet": {"properties": {"title": "Sheet 1", "index": 1}}}]}


def test_lark_sheets_client_batch_add_sheets_requests() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            request=request,
            json={
                "code": 0,
                "data": {
                    "replies": [
                        {"addSheet": {"properties": {"sheetId": "sheet-1"}}},
                        {"addSheet": {"properties": {"sheetId": "sheet-2"}}},
                    ]
                },
            },
        )

    async def run() -> list[str]:
        async with AsyncHttpClient(base_url="https://example.test", transport=httpx.MockTransport(handler)) as aclient:
            return await LarkSheetsAsyncClient(aclient).batch_add_sheets(
                "spreadsheet-1",
                ["Sheet 1", "Sheet 2"],
                start_index=2,
            )

    sheet_ids = asyncio.run(run())

    assert sheet_ids == ["sheet-1", "sheet-2"]
    assert requests[0].url.path == "/sheets/v2/spreadsheets/spreadsheet-1/sheets_batch_update"
    assert _request_json(requests[0]) == {
        "requests": [
            {"addSheet": {"properties": {"title": "Sheet 1", "index": 2}}},
            {"addSheet": {"properties": {"title": "Sheet 2", "index": 3}}},
        ]
    }


def test_lark_sheets_client_batch_add_sheets_rejects_empty_titles() -> None:
    async def run() -> None:
        async with AsyncHttpClient(base_url="https://example.test") as aclient:
            await LarkSheetsAsyncClient(aclient).batch_add_sheets("spreadsheet-1", [])

    with pytest.raises(ValidationError):
        asyncio.run(run())


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
                headers=["name", "value"],
                rows_values=[["alpha", 1]],
            )

    result = asyncio.run(run())

    assert result == (7, 2, 2)
    assert seen_payloads == [{"valueRange": {"range": "sheet-1!A1:B2", "values": [["name", "value"], ["alpha", 1]]}}]


def test_lark_sheets_client_overwrite_headers_only() -> None:
    seen_payloads: list[dict[str, Any]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen_payloads.append(_request_json(request))
        return httpx.Response(200, request=request, json={"code": 0, "data": {"revision": 7, "updatedRows": 1}})

    async def run() -> tuple[int, int, int]:
        async with AsyncHttpClient(base_url="https://example.test", transport=httpx.MockTransport(handler)) as aclient:
            return await LarkSheetsAsyncClient(aclient).overwrite_values(
                "spreadsheet-1",
                "sheet-1",
                headers=["name", "value"],
                rows_values=[],
            )

    result = asyncio.run(run())

    assert result == (7, 1, 2)
    assert seen_payloads == [{"valueRange": {"range": "sheet-1!A1:B1", "values": [["name", "value"]]}}]


def test_lark_sheets_client_query_values() -> None:
    requested_paths: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requested_paths.append(request.url.path)
        if "A1:CV1" in request.url.path:
            values = [["name", "value", None, "ignored"]]
        elif "A2:B501" in request.url.path:
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
        "/sheets/v2/spreadsheets/spreadsheet-1/values/sheet-1!A2:B501",
        "/sheets/v2/spreadsheets/spreadsheet-1/values/sheet-1!A502:B1001",
    ]


def test_lark_sheets_client_query_values_without_headers() -> None:
    requested_paths: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requested_paths.append(request.url.path)
        values = [["alpha", 1], ["beta", 2]] if "A1:B500" in request.url.path else []
        return httpx.Response(200, request=request, json={"code": 0, "data": {"valueRange": {"values": values}}})

    async def run() -> tuple[list[str], list[list[Any]]]:
        async with AsyncHttpClient(base_url="https://example.test", transport=httpx.MockTransport(handler)) as aclient:
            return await LarkSheetsAsyncClient(aclient).query_values(
                "spreadsheet-1",
                "sheet-1",
                start_row=1,
                end_col=2,
                has_headers=False,
            )

    headers, rows = asyncio.run(run())

    assert headers == []
    assert rows == [["alpha", 1], ["beta", 2]]
    assert requested_paths == [
        "/sheets/v2/spreadsheets/spreadsheet-1/values/sheet-1!A1:B500",
        "/sheets/v2/spreadsheets/spreadsheet-1/values/sheet-1!A501:B1000",
    ]


def test_lark_sheets_client_query_values_can_omit_returned_headers() -> None:
    requested_paths: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requested_paths.append(request.url.path)
        if "A1:CV1" in request.url.path:
            values = [["name", "value", None]]
        elif "A10:B509" in request.url.path:
            values = [["alpha", 1]]
        else:
            values = []
        return httpx.Response(200, request=request, json={"code": 0, "data": {"valueRange": {"values": values}}})

    async def run() -> tuple[list[str], list[list[Any]]]:
        async with AsyncHttpClient(base_url="https://example.test", transport=httpx.MockTransport(handler)) as aclient:
            return await LarkSheetsAsyncClient(aclient).query_values(
                "spreadsheet-1",
                "sheet-1",
                start_row=10,
                return_headers=False,
            )

    headers, rows = asyncio.run(run())

    assert headers == []
    assert rows == [["alpha", 1]]
    assert requested_paths == [
        "/sheets/v2/spreadsheets/spreadsheet-1/values/sheet-1!A1:CV1",
        "/sheets/v2/spreadsheets/spreadsheet-1/values/sheet-1!A10:B509",
        "/sheets/v2/spreadsheets/spreadsheet-1/values/sheet-1!A510:B1009",
    ]


def test_lark_sheet_backend_requires_lark_locator() -> None:
    backend = AsyncLarkSheetsBackend(LarkSheetsAsyncClient(AsyncHttpClient(base_url="https://example.test")))

    async def run() -> None:
        await backend.write_table(
            object(),
            headers=["name"],
            rows_values=[["alpha"]],
        )

    with pytest.raises(TypeError, match="AsyncLarkSheetsBackend requires LarkSheetsLocator"):
        asyncio.run(run())
