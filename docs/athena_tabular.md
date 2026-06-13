# athena tabular 使用指南

`athena_kit.core.tabular` 提供一组面向二维表格的模型、序列化和持久化抽象。它的目标不是绑定某一种存储，而是把 Excel、CSV、数据库查询结果、飞书表格、pandas DataFrame 等结构统一到一套简单的数据边界：

```python
headers: list[str]
rows_values: list[list[object]]
```

在这个边界之上，`TableRow` 负责把二维数据转换为 Pydantic 模型，`TableBackend` / `AsyncTableBackend` 负责适配外部存储，`TableRepository` / `AsyncTableRepository` 负责把模型和后端连接起来。

## 1. 安装

核心 tabular 能力随 `athena-kit` 默认安装。

```shell
uv add athena-kit
```

如果需要使用 pandas DataFrame 转换工具，需要安装 `dataframe` extra。

```shell
uv add "athena-kit[dataframe]"
```

## 2. 表格模型

一个表格模型通常继承 `TableRow`，并使用 `TableCell` 描述每一列的标题和顺序。

```python
from datetime import date

from athena_kit.core.tabular import TableCell, TableRow


class TradeRow(TableRow):
    trade_date: date = TableCell(title="日期", order=1)
    symbol: str = TableCell(title="代码", order=2)
    amount: int = TableCell(title="成交额", order=3)
    tags: list[str] = TableCell(title="标签", order=4, default_factory=list)
```

`TableCell` 本质上是带有表格元信息的 Pydantic `Field`，因此可以继续使用 `default`、`default_factory`、`alias` 等 Pydantic 字段参数。

```python
from pydantic import Field


class UserRow(TableRow):
    name: str = TableCell(title="姓名", order=1)
    age: int = TableCell(title="年龄", order=2, ge=0)
```

标题优先级是：

1. `TableCell(title=...)`
2. Pydantic field alias
3. 字段名

字段顺序由 `order` 控制，`order` 相同则按字段名排序。

## 3. 行与单元格转换

`TableRow.table_headers()` 会返回写入表格时使用的标题行。

```python
assert TradeRow.table_headers() == ["日期", "代码", "成交额", "标签"]
```

`to_table_row()` 会把模型实例序列化为一行单元格值。

```python
row = TradeRow(
    trade_date=date(2026, 6, 11),
    symbol="000001",
    amount=1200,
    tags=["core", "tabular"],
)

assert row.to_table_row() == ["2026-06-11", "000001", 1200, "core, tabular"]
```

`from_table_row()` 和 `from_table_rows()` 会根据标题行把单元格值反序列化为模型实例。

```python
headers = ["日期", "代码", "成交额", "标签"]
rows_values = [
    ["2026-06-11", "000001", "1200", "core, tabular"],
]

rows = TradeRow.from_table_rows(headers, rows_values)
assert rows[0].amount == 1200
assert rows[0].tags == ["core", "tabular"]
```

反序列化时会按标题映射字段，未知标题会被忽略。行数据比标题短时，缺失位置会按 `None` 处理，再交给 Pydantic 校验。

## 4. 单元格序列化规则

`serialize_cell_value()` 和 `deserialize_cell_value()` 是 `TableRow` 内部使用的单元格编解码函数，也可以直接调用。

```python
from athena_kit.core.tabular import deserialize_cell_value, serialize_cell_value

value = serialize_cell_value(["core", "tabular"], list[str])
assert value == "core, tabular"

items = deserialize_cell_value("core, tabular", list[str])
assert items == ["core", "tabular"]
```

常见规则：

- `None` 保持为空值
- `str` 会去除首尾空白
- `bool`、`int`、`float` 按标量处理
- `date`、`datetime`、`time` 会格式化为稳定字符串
- `list[str]`、`set[str]`、`tuple[str, ...]` 和固定长度的全字符串 tuple 会序列化为逗号分隔字符串
- 其他序列和 `dict` 会使用 JSON 字符串保存
- 空单元格和空白字符串在反序列化时会被视为 `None`

如果字段注解是 `list[int]`、`tuple[int, ...]`、`dict[str, int]` 等非字符串序列或字典，会走 JSON 路径，以便尽量保留结构和值类型。

## 5. 外部来源映射

`SourceCell` 用于描述外部数据结构到模型字段的映射。它不负责定义规范表格的标题和列顺序，而是用于导入 pandas DataFrame、CSV、数据库查询结果等外部数据。

```python
from datetime import date
from pydantic import BaseModel

from athena_kit.core.tabular import SourceCell


class TradeSource(BaseModel):
    trade_date: date = SourceCell(required=True)
    symbol: str = SourceCell(source=["证券代码", "代码"])
    amount: int = SourceCell(source="成交额", transform=int)
```

`source` 可以是单个列名，也可以是多个候选列名。`required=True` 表示严格要求来源中存在该字段。`transform` 会在模型校验前对读取到的值做转换。

## 6. pandas DataFrame 转换

安装 `athena-kit[dataframe]` 后，可以使用 pandas 转换工具。

```python
from datetime import date

import pandas as pd

from athena_kit.core.tabular import dataframe_to_models

df = pd.DataFrame([
    {"代码": "000001", "成交额": 1200},
])

rows = dataframe_to_models(
    df,
    TradeSource,
    extra_fields={"trade_date": date(2026, 6, 11)},
    strict=False,
)
```

`dataframe_to_models()` 会读取模型字段上的 `SourceCell` 元信息：

- 先按 `source` 中的候选列查找
- 找不到时尝试字段名
- 仍然找不到时，如果 `extra_fields` 提供了同名字段，则使用额外字段
- `strict=True` 或字段 `required=True` 时，缺失来源会抛出 `ValueError`

模型也可以转换回 DataFrame。

```python
from athena_kit.core.tabular import table_rows_to_dataframe

df = table_rows_to_dataframe([
    TradeRow(trade_date=date(2026, 6, 11), symbol="000001", amount=1200),
])

assert list(df.columns) == ["日期", "代码", "成交额", "标签"]
```

`table_rows_to_dataframe()` 对 `TableRow` 会使用 `table_headers()` 作为列名；对普通 Pydantic 模型会使用 `model_dump(by_alias=True)`。

## 7. 后端协议

`TableBackend` 和 `AsyncTableBackend` 是 `core.tabular` 与外部存储之间的边界。后端只处理原始二维数据，不感知 Pydantic 模型。

同步后端协议：

```python
from typing import Any

from athena_kit.core.tabular import TableBackend, TableLocator


class MyLocator:
    name: str


class MyBackend(TableBackend):
    def write_table(
        self,
        locator: TableLocator,
        headers: list[str] | None,
        rows_values: list[list[Any]],
        *,
        start_row: int = 1,
    ) -> tuple[int, int, int]:
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
        ...
```

异步后端使用 `AsyncTableBackend`，方法签名相同，但 `write_table()` 和 `read_table()` 是 async 方法。

`write_table()` 返回三元组：

- `version`：写入后的版本号或修订号；没有版本概念的后端可以返回自增计数、时间戳或固定值
- `written_rows`：写入的数据行数量
- `written_columns`：写入列数

`read_table()` 的 `has_headers` 和 `return_headers` 用于区分数据源是否有标题行，以及调用方是否需要返回标题行。

## 8. Repository

`TableRepository` 把同步 `TableBackend` 和 `TableRow` 连接起来；`AsyncTableRepository` 则连接异步后端。

```python
from athena_kit.core.tabular import TableRepository

repository = TableRepository(backend, locator, TradeRow)

repository.replace_all([
    TradeRow(trade_date=date(2026, 6, 11), symbol="000001", amount=1200),
])

rows = repository.list_all()
```

`replace_all()` 会从第 1 行开始写入标题行和数据行。`append()` 则从指定行开始写入数据行，不写标题。

```python
repository.append(
    [TradeRow(trade_date=date(2026, 6, 12), symbol="000002", amount=1800)],
    start_row=10,
)
```

默认情况下，`list_all()` 假设底层表格有标题行。如果数据源没有标题行，但列顺序和 `TableRow.table_headers()` 一致，可以设置 `has_headers=False`。

```python
rows = repository.list_all(has_headers=False, start_row=1)
```

异步仓储用法类似：

```python
from athena_kit.core.tabular import AsyncTableRepository

repository = AsyncTableRepository(async_backend, locator, TradeRow)
rows = await repository.list_all()
```

## 9. 与飞书 Sheets 结合

飞书 Sheets 后端实现位于 `athena_kit.lark.sheets`。它实现了 `AsyncTableBackend`，因此可以直接用于 `AsyncTableRepository`。

```python
from athena_kit.core.tabular import AsyncTableRepository
from athena_kit.lark.sheets import AsyncLarkSheetsBackend, LarkSheetsLocator

backend = AsyncLarkSheetsBackend(client.sheets)
locator = LarkSheetsLocator(
    spreadsheet_token="shtcn_xxx",
    sheet_id="sheet_xxx",
)

repository = AsyncTableRepository(backend, locator, TradeRow)
rows = await repository.list_all()
```

更多飞书 Sheets 用法见 [athena_lark.md](athena_lark.md)。

## 10. 模块边界

`core.tabular` 的推荐理解方式是：

- `cell.py`、`row.py`、`serialization.py`：表格模型层，定义单元格、一行模型和单元格值编解码
- `source.py`、`pandas.py`：外部来源映射和 DataFrame 转换
- `backend.py`：同步/异步二维表格后端协议
- `repository.py`：模型化读写入口

具体外部系统实现，例如飞书、Excel、数据库，应该实现 `TableBackend` 或 `AsyncTableBackend`，并放在对应 integration 模块中。`core.tabular` 只维护稳定的二维数据协议和模型转换规则。
