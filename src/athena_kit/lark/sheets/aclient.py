from collections.abc import Sequence
from datetime import datetime
from typing import Any
from uuid import uuid4

import httpx
from athena_kit.http import (
    create_biz_code_validator,
    extract_response_json_value,
    extract_response_json_values,
)
from athena_kit.lark.sheets.a1_notation import build_a1_range
from athena_kit.lark.sheets.requests import (
    SheetsBatchUpdateRequest,
    SheetUpdateRequest,
    SheetWritePayload,
    SheetWriteRequest,
)

_SHEETS_SUCCESS_VALIDATOR = create_biz_code_validator(
    code_key="code",
    success_codes=(0,),
    message_key="msg",
)


def _ensure_title(title: str | None) -> str:
    if title is None or not title.strip():
        return f"{datetime.now():%Y%m%d}_{uuid4().hex[:8]}"
    return title.strip()


class LarkSheetsAsyncClient:
    def __init__(self, aclient: httpx.AsyncClient):
        self._aclient = aclient

    async def create_spreadsheet(self, folder_token: str, title: str | None = None) -> tuple[str, str]:
        """在指定文件夹中创建飞书电子表格文档。

        Args:
            folder_token: 目标文件夹的 token。
            title: 新文档标题。传入 `None` 或空白字符串时，会自动生成 `YYYYMMDD_xxxxxxxx` 格式的随机标题，
                其中后缀来自 `uuid4().hex` 的前 8 位。

        Returns:
            新建电子表格的 spreadsheet_token 和访问 URL。

        References:
            https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet/create
        """
        response = await self._aclient.post(
            "/sheets/v3/spreadsheets",
            json={"folder_token": folder_token, "title": _ensure_title(title)},
        )
        spreadsheet_token, url = extract_response_json_values(
            response,
            ["data.spreadsheet.spreadsheet_token", "data.spreadsheet.url"],
            validator=_SHEETS_SUCCESS_VALIDATOR,
        )
        return (str(spreadsheet_token), str(url))

    async def batch_add_sheets(
        self,
        spreadsheet_token: str,
        sheet_titles: Sequence[str],
        start_index: int = 0,
    ) -> list[str]:
        """批量新增工作表。

        Args:
            spreadsheet_token: 目标电子表格的 token。
            sheet_titles: 要新增的工作表标题列表。标题会经过 `_ensure_title` 规范化；空白标题会自动生成。
            start_index: 第一个新增工作表的插入位置，后续工作表会按列表顺序依次递增。

        Returns:
            按 `sheet_titles` 顺序返回新增工作表的 sheet_id 列表。

        References:
            https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet-sheet/operate-sheets
        """
        request = SheetsBatchUpdateRequest(
            requests=[
                SheetUpdateRequest.add_sheet(
                    _ensure_title(title),
                    index,
                )
                for index, title in enumerate(sheet_titles, start=start_index)
            ]
        )
        response = await self._aclient.post(
            f"/sheets/v2/spreadsheets/{spreadsheet_token}/sheets_batch_update",
            json=request.model_dump(exclude_none=True),
        )
        payload_replies = extract_response_json_value(
            response,
            "data.replies",
            validator=_SHEETS_SUCCESS_VALIDATOR,
        )
        return [reply["addSheet"]["properties"]["sheetId"] for reply in payload_replies]  # pyright: ignore

    async def add_sheet(
        self,
        spreadsheet_token: str,
        sheet_title: str | None = None,
        sheet_index: int = 0,
    ) -> str:
        """新增单个工作表。

        Args:
            spreadsheet_token: 目标电子表格的 token。
            sheet_title: 新增工作表标题。传入 `None` 或空白字符串时，会自动生成默认标题。
            sheet_index: 新增工作表的插入位置。

        Returns:
            新增工作表的 sheet_id。

        References:
            https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet-sheet/operate-sheets
        """
        sheet_ids = await self.batch_add_sheets(spreadsheet_token, [_ensure_title(sheet_title)], sheet_index)
        return sheet_ids[0]

    async def create_spreadsheet_with_sheets(
        self,
        folder_token: str,
        spreadsheet_title: str | None,
        sheet_titles: Sequence[str],
    ) -> tuple[str, str, list[str]]:
        """创建电子表格文档，并批量新增工作表。

        先在指定文件夹中创建一个电子表格文档，再在新建文档中按 `sheet_titles` 顺序批量创建工作表。
        工作表从索引 0 开始插入。

        Args:
            folder_token: 目标文件夹的 token。
            spreadsheet_title: 新建电子表格文档标题。传入 `None` 或空白字符串时，会自动生成默认标题。
            sheet_titles: 要新增的工作表标题列表。标题会经过 `_ensure_title` 规范化；空白标题会自动生成。

        Returns:
            三元组，依次为新建电子表格的 spreadsheet_token、访问 URL、以及新增工作表的 sheet_id 列表。

        References:
            https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet/create
            https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet-sheet/operate-sheets
        """
        spreadsheet_token, url = await self.create_spreadsheet(folder_token, spreadsheet_title)
        sheet_ids = await self.batch_add_sheets(spreadsheet_token, sheet_titles, start_index=0)
        return spreadsheet_token, url, sheet_ids

    async def overwrite_values(
        self,
        spreadsheet_token: str,
        sheet_id: str,
        *,
        headers: list[str] | None = None,
        rows_values: list[list[object]],
        start_row: int = 1,
    ) -> tuple[int, int, int]:
        """覆盖写入单个工作表范围内的单元格值。

        根据 `headers`、`rows_values`、`start_row` 自动构造 A1 notation 写入范围。
        `start_row == 1` 且传入 `headers` 时会一并写入标题行；`start_row > 1` 时只写入数据行。
        允许只写标题，也允许数据行列数 超过标题列数。

        Args:
            spreadsheet_token: 目标电子表格的 token。
            sheet_id: 目标工作表 ID。
            headers: 可选标题行。传入 `None` 时不会写入标题。
            rows_values: 要写入的数据行。可以为空，但不能和 `headers` 同时为空。
            start_row: 起始写入行号，从 1 开始。大于 1 时，不会写入 `headers`。

        Returns:
            三元组，依次为飞书表格更新后的 revision、实际更新的总行数、以及本次写入范围的列数。

        References:
            https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/write-data-to-a-single-range
        """
        if start_row < 1:
            raise ValueError("`start_row` must be greater than or equal to 1.")
        if not rows_values and not headers:
            raise ValueError("`headers` and `rows_values` cannot be all empty.")

        include_headers = start_row == 1 and headers is not None  # 是否写入标题
        write_payload = SheetWritePayload.from_rows_values(headers=headers, rows_values=rows_values)
        n_rows, n_cols = write_payload.shape(include_headers)
        write_2dvalues = write_payload.to_table_2dvalues(include_headers)

        max_rows_per_request = 4000  # 单次最多写入 4000 行
        revision = 0
        updated_rows = 0
        for start_idx in range(0, n_rows, max_rows_per_request):
            end_idx = min(start_idx + max_rows_per_request, n_rows)
            batch_write_2d_values = write_2dvalues[start_idx:end_idx]

            write_range = build_a1_range(
                sheet_id,
                n_rows=end_idx - start_idx,
                n_cols=n_cols,
                start_row=start_row + start_idx,
            )
            request = SheetWriteRequest.build(write_range, batch_write_2d_values)
            response = await self._aclient.put(
                f"/sheets/v2/spreadsheets/{spreadsheet_token}/values",
                json=request.model_dump(),
            )

            revision, batch_updated_rows = extract_response_json_values(
                response,
                ["data.revision", "data.updatedRows"],
                validator=_SHEETS_SUCCESS_VALIDATOR,
            )
            if not isinstance(revision, int) or not isinstance(batch_updated_rows, int):
                raise ValueError("The Lark API is responding incorrectly.")

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
        has_headers: bool = True,
        return_headers: bool = True,
    ) -> tuple[list[str], list[list[Any]]]:
        """查询工作表中的单元格值。

        默认按“第 1 行是标题行、第 2 行开始是数据行”的表格结构读取。
        对于没有标题行的工作表，可以传入 `has_headers=False` 并从 `start_row=1` 开始读取全部数据。

        Args:
            spreadsheet_token: 目标电子表格的 token。
            sheet_id: 目标工作表 ID。
            start_row: 数据起始行号，从 1 开始。
            end_row: 数据结束行号，从 1 开始。为 `None` 时会分页(单批次 500 行)读取，直到遇到空批次。
            start_col: 起始列号，从 1 开始。
            end_col: 结束列号，从 1 开始。为 `None` 时，有标题行时按标题列数读取；无标题行时最多读取 100 列。
            has_headers: 工作表是否存在标题行。标题行固定为第 1 行。
            return_headers: 是否在返回值的第一项中返回标题行。`has_headers=False` 时始终返回空标题列表。

        Returns:
            二元组，依次为标题列表和数据行二维列表。若 `return_headers=False` 或 `has_headers=False`，标题列表为空。

        References:
            https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/reading-a-single-range
        """
        if start_row < 1:
            raise ValueError("start_row must be greater than or equal to 1")
        if end_row is not None and end_row < start_row:
            raise ValueError("end_row must be greater than or equal to start_row")
        if start_col < 1:
            raise ValueError("start_col must be greater than or equal to 1")
        if end_col is not None and end_col < start_col:
            raise ValueError("end_col must be greater than or equal to start_col")

        n_cols = end_col - start_col + 1 if end_col is not None else 100
        if n_cols > 100:
            raise ValueError("Query columns must be less than or equal to 100.")

        headers: list[str] = []
        if has_headers:
            headers = await self._query_headers(
                spreadsheet_token=spreadsheet_token,
                sheet_id=sheet_id,
                start_col=start_col,
                n_cols=n_cols,
            )
            if not headers:
                raise ValueError("No valid headers found.")
            if end_col is None:  # 如果 end_col 为空，按照标题行修正 n_cols
                n_cols = len(headers)

        rows_values: list[list[object]] = []
        max_rows_per_request = 500  # 单批次最多 500 行
        current_start_row = start_row

        while end_row is None or current_start_row <= end_row:
            n_rows = (
                max_rows_per_request if end_row is None else min(end_row - current_start_row + 1, max_rows_per_request)
            )
            query_range = build_a1_range(
                sheet_id,
                n_rows=n_rows,
                n_cols=n_cols,
                start_row=current_start_row,
                start_col=start_col,
            )
            response = await self._aclient.get(
                f"/sheets/v2/spreadsheets/{spreadsheet_token}/values/{query_range}",
            )
            raw_rows_values = extract_response_json_value(
                response,
                "data.valueRange.values",
                validator=_SHEETS_SUCCESS_VALIDATOR,
            )
            if not raw_rows_values:  # 没有查询到数据行
                break
            if not isinstance(raw_rows_values, list):
                raise TypeError("Lark query response values should be a list.")

            batch_rows_values = [
                row_values
                for row_values in raw_rows_values
                if isinstance(row_values, list) and not all(value is None for value in row_values)
            ]
            if not batch_rows_values:
                break

            rows_values.extend(batch_rows_values)  # pyright: ignore[reportArgumentType]
            current_start_row += n_rows

        return headers if has_headers and return_headers else [], rows_values

    async def _query_headers(
        self,
        spreadsheet_token: str,
        sheet_id: str,
        *,
        start_col: int = 1,
        n_cols: int,
    ) -> list[str]:
        query_range = build_a1_range(sheet_id, n_rows=1, n_cols=n_cols, start_row=1, start_col=start_col)
        response = await self._aclient.get(
            f"/sheets/v2/spreadsheets/{spreadsheet_token}/values/{query_range}",
        )

        raw_headers = extract_response_json_value(
            response,
            "data.valueRange.values",
            validator=_SHEETS_SUCCESS_VALIDATOR,
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
