from athena_kit.core.tabular.backend import AsyncTableBackend, TableBackend, TableLocator
from athena_kit.core.tabular.row import TableRow


class TableRepository[T: TableRow]:
    """同步表格模型仓储。

    `TableRepository` 将 `TableRow` 模型和同步 `TableBackend` 连接起来。
    它负责在模型对象和 `headers + rows_values` 之间转换，具体数据读写由后端实现完成。
    """

    def __init__(self, backend: TableBackend, locator: TableLocator, row_type: type[T]):
        self._backend = backend
        self._locator = locator
        self._row_type = row_type

    def list_all(
        self,
        *,
        start_row: int | None = None,
        end_row: int | None = None,
        start_col: int = 1,
        end_col: int | None = None,
        has_headers: bool = True,
    ) -> list[T]:
        """读取数据行并反序列化为表格模型列表。

        `has_headers` 为 `True` 时，底层表格需要提供标题行，仓储会使用读取到的标题行进行字段映射。
        `has_headers` 为 `False` 时，底层表格不包含标题行，仓储会使用 `TableRow.table_headers()` 作为列顺序。
        """
        start_row = start_row if start_row is not None else 2 if has_headers else 1
        headers, rows_values = self._backend.read_table(
            self._locator,
            start_row=start_row,
            end_row=end_row,
            start_col=start_col,
            end_col=end_col,
            has_headers=has_headers,
            return_headers=has_headers,
        )

        if not rows_values:
            return []

        if not has_headers:
            headers = self._row_type.table_headers()
        if not headers:
            return []

        return self._row_type.from_table_rows(headers, rows_values)

    def replace_all(self, rows: list[T]) -> tuple[int, int, int]:
        """用给定模型列表覆盖整张表格，写入标题行和数据行。"""
        return self._backend.write_table(
            locator=self._locator,
            headers=self._row_type.table_headers(),
            rows_values=[row.to_table_row() for row in rows],
            start_row=1,
        )

    def append(self, rows: list[T], *, start_row: int) -> tuple[int, int, int]:
        """从指定行开始追加模型数据，不写入标题行。"""
        return self._backend.write_table(
            locator=self._locator,
            headers=None,
            rows_values=[row.to_table_row() for row in rows],
            start_row=start_row,
        )


class AsyncTableRepository[T: TableRow]:
    """异步表格模型仓储。

    `AsyncTableRepository` 将 `TableRow` 模型和异步 `AsyncTableBackend` 连接起来。
    它负责在模型对象和 `headers + rows_values` 之间转换，具体数据读写由后端实现完成。
    """

    def __init__(self, backend: AsyncTableBackend, locator: TableLocator, row_type: type[T]):
        self._backend = backend
        self._locator = locator
        self._row_type = row_type

    async def list_all(
        self,
        *,
        start_row: int | None = None,
        end_row: int | None = None,
        start_col: int = 1,
        end_col: int | None = None,
        has_headers: bool = True,
    ) -> list[T]:
        """异步读取数据行并反序列化为表格模型列表。

        `has_headers` 为 `True` 时，底层表格需要提供标题行，仓储会使用读取到的标题行进行字段映射。
        `has_headers` 为 `False` 时，底层表格不包含标题行，仓储会使用 `TableRow.table_headers()` 作为列顺序。
        """
        start_row = start_row if start_row is not None else 2 if has_headers else 1
        headers, rows_values = await self._backend.read_table(
            self._locator,
            start_row=start_row,
            end_row=end_row,
            start_col=start_col,
            end_col=end_col,
            has_headers=has_headers,
            return_headers=has_headers,
        )

        if not rows_values:
            return []

        if not has_headers:
            headers = self._row_type.table_headers()
        if not headers:
            return []

        return self._row_type.from_table_rows(headers, rows_values)

    async def replace_all(self, rows: list[T]) -> tuple[int, int, int]:
        """异步用给定模型列表覆盖整张表格，写入标题行和数据行。"""
        return await self._backend.write_table(
            locator=self._locator,
            headers=self._row_type.table_headers(),
            rows_values=[row.to_table_row() for row in rows],
            start_row=1,
        )

    async def append(self, rows: list[T], *, start_row: int) -> tuple[int, int, int]:
        """异步从指定行开始追加模型数据，不写入标题行。"""
        return await self._backend.write_table(
            locator=self._locator,
            headers=None,
            rows_values=[row.to_table_row() for row in rows],
            start_row=start_row,
        )
