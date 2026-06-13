from dataclasses import dataclass
from typing import Any

from athena_kit.core.tabular import AsyncTableBackend, TableLocator
from athena_kit.lark.sheets import LarkSheetsAsyncClient


@dataclass(slots=True)
class LarkSheetsLocator:
    spreadsheet_token: str
    sheet_id: str


def _ensure_lark_locator(locator: TableLocator) -> LarkSheetsLocator:
    if not isinstance(locator, LarkSheetsLocator):
        raise TypeError(f"AsyncLarkSheetsBackend requires LarkSheetsLocator, got {type(locator).__name__}.")
    return locator


class AsyncLarkSheetsBackend(AsyncTableBackend):
    def __init__(self, aclient: LarkSheetsAsyncClient):
        self._aclient = aclient

    async def write_table(
        self,
        locator: TableLocator,
        headers: list[str] | None,
        rows_values: list[list[Any]],
        *,
        start_row: int = 1,
    ) -> tuple[int, int, int]:
        lark_locator = _ensure_lark_locator(locator)

        return await self._aclient.overwrite_values(
            spreadsheet_token=lark_locator.spreadsheet_token,
            sheet_id=lark_locator.sheet_id,
            headers=headers,
            rows_values=rows_values,
            start_row=start_row,
        )

    async def read_table(
        self,
        locator: TableLocator,
        *,
        start_row: int = 2,
        end_row: int | None = None,
        start_col: int = 1,
        end_col: int | None = None,
        has_headers: bool = True,
        return_headers: bool = True,
    ) -> tuple[list[str], list[list[Any]]]:
        lark_locator = _ensure_lark_locator(locator)

        return await self._aclient.query_values(
            spreadsheet_token=lark_locator.spreadsheet_token,
            sheet_id=lark_locator.sheet_id,
            start_row=start_row,
            end_row=end_row,
            start_col=start_col,
            end_col=end_col,
            has_headers=has_headers,
            return_headers=return_headers,
        )
