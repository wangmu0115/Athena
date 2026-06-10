from datetime import datetime
from typing import Any

from athena_kit.http import AsyncHttpClient, extract_response_json_value, extract_response_json_values
from athena_kit.lark.models.sheets import (
    CreateSpreadsheetRequest,
    SheetsBatchUpdateRequest,
    SheetUpdateRequest,
    SheetWriteRequest,
)
from athena_kit.lark.sheet.constants import (
    CREATE_SPREADSHEET_API_URL,
    OPERATE_SHEET_API_URL,
    READ_SINGLE_RANGE_API_URL,
    WRITE_SINGLE_RANGE_API_URL,
)
from athena_kit.lark.sheet.models import SheetWritePayload
from athena_kit.lark.sheet.range import calculate_range
from athena_kit.lark.validators import LARK_SUCCESS_VALIDATOR


class LarkSheetClient:
    """Low-level Lark Sheet API client."""

    def __init__(self, aclient: AsyncHttpClient):
        self._aclient = aclient

    async def create_spreadsheet(
        self,
        folder_token: str,
        title: str | None = None,
    ) -> tuple[str, str]:
        title = title or datetime.now().strftime("%Y%m%d_%H%M%S")
        request = CreateSpreadsheetRequest(folder_token=folder_token, title=title)
        response = await self._aclient.post(CREATE_SPREADSHEET_API_URL, json=request.model_dump())

        spreadsheet_token, url = extract_response_json_values(
            response,
            ["data.spreadsheet.spreadsheet_token", "data.spreadsheet.url"],
            validator=LARK_SUCCESS_VALIDATOR,
        )
        if not isinstance(spreadsheet_token, str) or not isinstance(url, str):
            raise TypeError("Lark create spreadsheet response should contain spreadsheet_token and url strings.")
        return spreadsheet_token, url

    async def add_sheet(
        self,
        spreadsheet_token: str,
        sheet_title: str | None = None,
        sheet_index: int = 0,
    ) -> str:
        sheet_title = sheet_title or datetime.now().strftime("%Y%m%d_%H%M%S")
        sheet_request = SheetUpdateRequest.add_sheet(sheet_title, sheet_index)
        request = SheetsBatchUpdateRequest(requests=[sheet_request])
        response = await self._aclient.post(
            OPERATE_SHEET_API_URL(spreadsheet_token),
            json=request.model_dump(exclude_none=True),
        )
        sheet_id = extract_response_json_value(
            response,
            "data.replies[0].addSheet.properties.sheetId",
            validator=LARK_SUCCESS_VALIDATOR,
        )
        if not isinstance(sheet_id, str):
            raise TypeError("Lark add sheet response should contain a sheetId string.")
        return sheet_id

    async def overwrite_values(
        self,
        spreadsheet_token: str,
        sheet_id: str,
        *,
        value_headers: list[str] | None = None,
        rows_values: list[list[Any]],
        start_row: int = 1,
    ) -> tuple[int, int, int]:
        if start_row < 1:
            raise ValueError("start_row must be greater than or equal to 1.")
        if not rows_values:
            raise ValueError("rows_values cannot be empty.")

        include_headers = start_row == 1 and value_headers is not None
        write_payload = SheetWritePayload.from_rows_values(headers=value_headers, rows_values=rows_values)
        n_rows, n_cols = write_payload.shape(include_headers)
        write_2dvalues = write_payload.to_table_2dvalues(include_headers)

        max_rows_per_request = 2000
        revision = 0
        updated_rows = 0
        for start_idx in range(0, n_rows, max_rows_per_request):
            end_idx = min(start_idx + max_rows_per_request, n_rows)
            batch_write_2d_values = write_2dvalues[start_idx:end_idx]
            write_range = calculate_range(
                sheet_id,
                n_rows=end_idx - start_idx,
                n_cols=n_cols,
                start_row=start_row + start_idx,
            )
            request = SheetWriteRequest.build(write_range, batch_write_2d_values)
            response = await self._aclient.put(
                WRITE_SINGLE_RANGE_API_URL(spreadsheet_token),
                json=request.model_dump(),
            )
            batch_revision, batch_updated_rows = extract_response_json_values(
                response,
                ["data.revision", "data.updatedRows"],
                validator=LARK_SUCCESS_VALIDATOR,
            )
            if not isinstance(batch_revision, int) or not isinstance(batch_updated_rows, int):
                raise TypeError("Lark write response should contain integer revision and updatedRows.")
            revision = batch_revision
            updated_rows += batch_updated_rows

        return revision, updated_rows, n_cols

    async def query_values(
        self,
        spreadsheet_token: str,
        sheet_id: str,
        *,
        start_row: int = 2,
        end_row: int | None = None,
        start_col: int = 1,
        end_col: int | None = None,
    ) -> tuple[list[str], list[list[Any]]]:
        if start_row < 2:
            raise ValueError("start_row must be greater than or equal to 2")
        if end_row is not None and end_row < start_row:
            raise ValueError("end_row must be greater than or equal to start_row")
        if start_col < 1:
            raise ValueError("start_col must be greater than or equal to 1")
        if end_col is not None and end_col < start_col:
            raise ValueError("end_col must be greater than or equal to start_col")

        headers = await self._query_headers(
            spreadsheet_token=spreadsheet_token,
            sheet_id=sheet_id,
            start_col=start_col,
            end_col=end_col,
        )
        if not headers:
            raise ValueError("No valid headers found.")

        rows_values: list[list[Any]] = []
        n_cols = len(headers)
        max_rows_per_request = 1000
        current_start_row = start_row
        while end_row is None or current_start_row <= end_row:
            n_rows = (
                max_rows_per_request
                if end_row is None
                else min(end_row - current_start_row + 1, max_rows_per_request)
            )
            query_range = calculate_range(
                sheet_id,
                n_rows=n_rows,
                n_cols=n_cols,
                start_row=current_start_row,
                start_col=start_col,
            )
            response = await self._aclient.get(READ_SINGLE_RANGE_API_URL(spreadsheet_token, query_range))
            raw_rows_values = extract_response_json_value(
                response,
                "data.valueRange.values",
                validator=LARK_SUCCESS_VALIDATOR,
            )
            if raw_rows_values is None:
                raw_rows_values = []
            if not isinstance(raw_rows_values, list):
                raise TypeError("Lark query response values should be a list.")

            batch_rows_values = [
                row_values
                for row_values in raw_rows_values
                if isinstance(row_values, list) and not all(value is None for value in row_values)
            ]
            if not batch_rows_values:
                break

            rows_values.extend(batch_rows_values)
            current_start_row += n_rows

        return headers, rows_values

    async def _query_headers(
        self,
        spreadsheet_token: str,
        sheet_id: str,
        *,
        start_col: int = 1,
        end_col: int | None = None,
    ) -> list[str]:
        n_cols = end_col - start_col + 1 if end_col is not None else 100
        if n_cols > 100:
            raise ValueError("Query columns must be less than or equal to 100.")

        query_range = calculate_range(
            sheet_id,
            n_rows=1,
            n_cols=n_cols,
            start_row=1,
            start_col=start_col,
        )
        response = await self._aclient.get(READ_SINGLE_RANGE_API_URL(spreadsheet_token, query_range))
        raw_headers = extract_response_json_value(
            response,
            "data.valueRange.values",
            validator=LARK_SUCCESS_VALIDATOR,
        )
        if not raw_headers:
            return []
        if not isinstance(raw_headers, list) or not raw_headers or not isinstance(raw_headers[0], list):
            raise TypeError("Lark header response values should be a non-empty list of rows.")

        headers = []
        for header in raw_headers[0]:
            if header is None or str(header).strip() == "":
                break
            headers.append(str(header).strip())
        return headers
