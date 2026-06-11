from typing import Any, Protocol


class TableLocator(Protocol):
    """定位具体二维表格的标记协议，只负责携带定位信息，不限定具体字段，不同后端可以定义自己的 Locator。

    Lark Sheet 可以包含 `spreadsheet_token` 和 `sheet_id`，
    Excel 可以包含文件路径和 sheet 名称，
    Database 可以包含连接信息和表名。
    """


class TableBackend(Protocol):
    """同步二维表格持久化后端协议，是 `athena_kit.core.tabular` 与外部存储系统之间的边界。

    只处理朴素的二维表格数据，即标题行 `headers` 和数据行 `rows_values`，
    不感知 `TableRow`、Pydantic 模型、字段校验或单元格序列化规则。

    具体后端实现可以来自飞书表格、Excel、CSV、数据库查询结果或其他表格型存储。
    实现者需要把外部系统的数据读写能力适配成统一的 `headers + rows_values` 结构，
    上层的 `TableRepository` 再负责把这些二维数据转换成表格模型。
    """

    def write_table(
        self,
        locator: TableLocator,
        headers: list[str] | None,
        rows_values: list[list[Any]],
        *,
        start_row: int = 1,
    ) -> tuple[int, int, int]:
        """将标题行和数据行写入指定表格。

        `headers` 为 `None` 时表示本次写入不包含标题行，只写入 `rows_values`。
        `headers` 为列表时表示需要先写入标题行，再写入数据行。
        `rows_values` 允许为空，因此后端需要支持只写标题的场景。

        `start_row` 使用 1-based 行号，表示本次写入从目标表格的第几行开始。

        返回值约定为 `(version, written_rows, written_columns)`
        - `version` 是写入完成后的表格版本号或修订号，没有版本概念的后端可以返回自增计数、时间戳或固定值
        - `written_rows` 是写入的数据行数量
        - `written_columns` 是写入列数
        """
        ...

    def read_table(
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
        """从指定表格读取标题行和数据行。

        `start_row`、`end_row`、`start_col` 和 `end_col` 都使用 1-based 坐标。
        `end_row` 或 `end_col` 为 `None` 时表示读取到后端可识别的有效末尾。

        `has_headers` 表示目标表格是否存在标题行。
        - `has_headers = True` 时，后端会把第 1 行作为标题行，从 `start_row` 指定的数据起始行读取数据。
        - `has_headers = False` 时，后端不会尝试读取标题行。

        `return_headers` 表示返回结果中是否包含标题行。
        为 `False` 时，返回的 `headers` 应为空列表，但不影响后端根据 `has_headers` 判断数据起始位置。

        返回值为 `(headers, rows_values)`
        - `headers` 是读取到的标题行。对于没有标题行或不需要返回标题行的表格，后端会返回空列表，
          由调用方决定如何解释数据行。
        - `rows_values` 是数据行。
        """
        ...


class AsyncTableBackend(Protocol):
    """异步二维表格持久化后端协议。

    `AsyncTableBackend` 与 `TableBackend` 的数据契约完全一致，只是读写方法为 async 方法。

    只处理朴素的二维表格数据，即标题行 `headers` 和数据行 `rows_values`，
    不感知 `TableRow`、Pydantic 模型、字段校验或单元格序列化规则。

    具体后端实现可以来自飞书表格、Excel、CSV、数据库查询结果或其他表格型存储。
    实现者需要把外部系统的数据读写能力适配成统一的 `headers + rows_values` 结构，
    上层的 `TableRepository` 再负责把这些二维数据转换成表格模型。
    """

    async def write_table(
        self,
        locator: TableLocator,
        headers: list[str] | None,
        rows_values: list[list[Any]],
        *,
        start_row: int = 1,
    ) -> tuple[int, int, int]:
        """异步将标题行和数据行写入指定表格。

        参数和返回值语义与 `TableBackend.write_table` 一致。
        """
        ...

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
        """异步从指定表格读取标题行和数据行。

        参数和返回值语义与 `TableBackend.read_table` 一致。
        """
        ...
