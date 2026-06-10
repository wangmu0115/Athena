from dataclasses import dataclass
from typing import Any

from athena_kit.core.tabular import TableLocator
from athena_kit.lark.sheet import LarkSheetClient


@dataclass(slots=True)
class LarkSheetLocator:
    spreadsheet_token: str
    sheet_id: str


class LarkSheetBackend:
    def __init__(self, client: LarkSheetClient):
        self._client = client

    async def write_table(
        self,
        locator: TableLocator,
        headers: list[str] | None,
        rows_values: list[list[Any]],
        *,
        start_row: int = 1,
    ) -> tuple[int, int, int]:
        lark_locator = self._ensure_lark_locator(locator)

        return await self._client.overwrite_values(
            spreadsheet_token=lark_locator.spreadsheet_token,
            sheet_id=lark_locator.sheet_id,
            value_headers=headers,
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
    ) -> tuple[list[str], list[list[Any]]]:
        lark_locator = self._ensure_lark_locator(locator)

        return await self._client.query_values(
            spreadsheet_token=lark_locator.spreadsheet_token,
            sheet_id=lark_locator.sheet_id,
            start_row=start_row,
            end_row=end_row,
            start_col=start_col,
            end_col=end_col,
        )

    @staticmethod
    def _ensure_lark_locator(locator: TableLocator) -> LarkSheetLocator:
        if not isinstance(locator, LarkSheetLocator):
            raise TypeError(f"LarkSheetBackend requires LarkSheetLocator, got {type(locator).__name__}.")
        return locator
