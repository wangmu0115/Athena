from athena_core.tabular.backend import TableBackend, TableLocator
from athena_core.tabular.schema import BaseTableRow


class TableRepository[T: BaseTableRow]:
    def __init__(self, backend: TableBackend, locator: TableLocator, row_type: type[T]):
        self._backend = backend
        self._locator = locator
        self._row_type = row_type

    async def list_all(self) -> list[T]:
        headers, rows_values = await self._backend.read_table(self._locator)

        if not headers or not rows_values:
            return []

        return self._row_type.from_rows_values(headers, rows_values)

    async def replace_all(self, rows: list[T]) -> tuple[int, int, int]:
        return await self._backend.write_table(
            locator=self._locator,
            headers=self._row_type.headers(),
            rows_values=[row.to_row_values() for row in rows],
            start_row=1,
        )

    async def append(self, rows: list[T], *, start_row: int) -> tuple[int, int, int]:
        return await self._backend.write_table(
            locator=self._locator,
            headers=None,
            rows_values=[row.to_row_values() for row in rows],
            start_row=start_row,
        )
