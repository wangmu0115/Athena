from typing import Any, Protocol


class TableLocator(Protocol):
    """Marker protocol for locating a concrete table."""


class TableBackend(Protocol):
    """Storage interface for tabular persistence."""

    async def write_table(
        self,
        locator: TableLocator,
        headers: list[str] | None,
        rows_values: list[list[Any]],
        *,
        start_row: int = 1,
    ) -> tuple[int, int, int]: ...

    async def read_table(
        self,
        locator: TableLocator,
        *,
        start_row: int = 2,
        end_row: int | None = None,
        start_col: int = 1,
        end_col: int | None = None,
    ) -> tuple[list[str], list[list[Any]]]: ...
