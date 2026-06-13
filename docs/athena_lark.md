# athena lark 使用指南

`athena_kit.lark` 提供飞书开放平台相关的轻量封装。当前模块重点支持 Sheets 场景，包括创建电子表格、批量新增工作表、读写单个工作表范围，以及把飞书表格接入 `athena_kit.core.tabular` 的表格仓储抽象。

这个模块不会重新实现一套 HTTP 客户端。底层请求仍然基于 `athena_kit.http.AsyncHttpClient` 和 HTTPX，认证、超时、日志、请求 ID、响应状态检查等能力沿用 `athena_kit.http` 的配置方式。

## 1. 安装

`athena-kit` 要求 Python 3.12 或更高版本。使用飞书扩展时，需要安装 `lark` extra。

```shell
uv add "athena-kit[lark]"
```

如果还需要把飞书表格数据转换为 pandas DataFrame，可以同时安装 `dataframe` extra。

```shell
uv add "athena-kit[lark,dataframe]"
```

安装后可以通过下面的方式确认 Lark Sheets 模块可用：

```python
from athena_kit.lark import AsyncLarkClient
from athena_kit.lark.sheets import LarkSheetsAsyncClient
```

## 2. 创建客户端

最常用的入口是 `AsyncLarkClient`。它会自动创建 tenant access token 认证器，并在内部注册 `sheets` 资源客户端。

```python
from athena_kit.lark import AsyncLarkClient


async def main() -> None:
    async with AsyncLarkClient(
        app_id="cli_xxx",
        app_secret="xxx",
        request_id=True,
        logging=True,
        response_status=True,
    ) as client:
        spreadsheet_token, url = await client.sheets.create_spreadsheet(
            folder_token="fldcn_xxx",
            title="每日数据",
        )
        print(spreadsheet_token, url)
```

`AsyncLarkClient` 的 `base_url` 默认是 `https://open.feishu.cn/open-apis`，`tenant_access_token_url` 默认使用飞书 tenant access token 内部应用接口。`timeout`、`request_id`、`logging`、`response_status` 和 `event_hooks` 会透传给底层 `AsyncHttpClient`。

如果你的项目已经有自己的 HTTPX 异步客户端，或者需要绕过 Athena HTTP 封装，也可以直接创建
`LarkSheetsAsyncClient`。

```python
from httpx import AsyncClient

from athena_kit.lark.auth import LarkTenantAccessTokenAuth
from athena_kit.lark.sheets import LarkSheetsAsyncClient


async def main() -> None:
    async with AsyncClient(
        base_url="https://open.feishu.cn/open-apis",
        auth=LarkTenantAccessTokenAuth("cli_xxx", "xxx"),
    ) as http_client:
        sheets = LarkSheetsAsyncClient(http_client)
        spreadsheet_token, url = await sheets.create_spreadsheet("fldcn_xxx", "数据表")
```

## 3. Sheets 文档和工作表

### 3.1. 创建电子表格

`create_spreadsheet()` 会在指定文件夹下创建飞书电子表格文档，返回 `spreadsheet_token` 和访问 URL。

```python
spreadsheet_token, url = await client.sheets.create_spreadsheet(
    folder_token="fldcn_xxx",
    title="交易汇总",
)
```

`title` 可以传入 `None` 或空白字符串，此时会自动生成 `YYYYMMDD_xxxxxxxx` 格式的标题。

### 3.2. 新增单个工作表

`add_sheet()` 用于在已有电子表格中新增一个工作表。

```python
sheet_id = await client.sheets.add_sheet(
    spreadsheet_token="shtcn_xxx",
    sheet_title="2026-06-11",
    sheet_index=0,
)
```

`sheet_index` 从 0 开始。标题同样支持传入 `None` 或空白字符串，模块会自动生成默认标题。

### 3.3. 批量新增工作表

`batch_add_sheets()` 用于一次新增多个工作表，返回值按传入标题顺序返回对应的 `sheet_id`。

```python
sheet_ids = await client.sheets.batch_add_sheets(
    spreadsheet_token="shtcn_xxx",
    sheet_titles=["日频", "周频", "月频"],
    start_index=0,
)
```

`start_index` 是第一个工作表的插入位置，后续工作表会按列表顺序依次递增。

### 3.4. 创建电子表格并新增多个工作表

`create_spreadsheet_with_sheets()` 适合创建文档后立即准备多个工作表的场景。

```python
spreadsheet_token, url, sheet_ids = await client.sheets.create_spreadsheet_with_sheets(
    folder_token="fldcn_xxx",
    spreadsheet_title="行情数据",
    sheet_titles=["raw", "clean", "report"],
)
```

返回值依次是新建电子表格的 `spreadsheet_token`、访问 URL 和新增工作表的 `sheet_id` 列表。

## 4. 写入工作表数据

`overwrite_values()` 用于覆盖写入单个工作表范围。它会根据 `headers`、`rows_values`、`start_row` 自动构造 A1 notation 范围。

```python
revision, updated_rows, updated_columns = await client.sheets.overwrite_values(
    spreadsheet_token="shtcn_xxx",
    sheet_id="sheet_xxx",
    headers=["日期", "代码", "成交额"],
    rows_values=[
        ["2026-06-11", "000001", 1200],
        ["2026-06-11", "000002", 1800],
    ],
    start_row=1,
)
```

返回值是三元组：

- `revision`：飞书表格更新后的 revision
- `updated_rows`：实际更新的总行数
- `updated_columns`：本次写入范围的列数

当 `start_row == 1` 且传入 `headers` 时，会先写标题行，再写数据行。`rows_values` 可以为空，因此可以只写标题。

```python
await client.sheets.overwrite_values(
    spreadsheet_token="shtcn_xxx",
    sheet_id="sheet_xxx",
    headers=["日期", "代码", "成交额"],
    rows_values=[],
    start_row=1,
)
```

当 `headers=None` 时，只写数据行。这适合追加或覆盖某个无标题区域。

```python
await client.sheets.overwrite_values(
    spreadsheet_token="shtcn_xxx",
    sheet_id="sheet_xxx",
    headers=None,
    rows_values=[["2026-06-12", "000001", 1300]],
    start_row=10,
)
```

`rows_values` 的列数允许超过 `headers` 的长度。这个设计用于支持某些业务场景中固定标题后追加可选补充值。

## 5. 读取工作表数据

`query_values()` 用于读取单个工作表中的单元格值。默认按“第 1 行是标题行、第 2 行开始是数据行”的结构读取。

```python
headers, rows_values = await client.sheets.query_values(
    spreadsheet_token="shtcn_xxx",
    sheet_id="sheet_xxx",
)
```

如果只读取某个范围，可以指定行列边界。行号和列号都从 1 开始。

```python
headers, rows_values = await client.sheets.query_values(
    spreadsheet_token="shtcn_xxx",
    sheet_id="sheet_xxx",
    start_row=10,
    end_row=50,
    start_col=1,
    end_col=3,
)
```

`end_row=None` 时会按批次分页读取，每批最多 500 行，直到遇到空批次。`end_col=None` 时，如果表格有标题行，会按标题列数读取；如果没有标题行，最多读取 100 列。

### 5.1. 无标题表格

如果目标工作表没有标题行，可以设置 `has_headers=False`，并通常把 `start_row` 设为 1。

```python
headers, rows_values = await client.sheets.query_values(
    spreadsheet_token="shtcn_xxx",
    sheet_id="sheet_xxx",
    start_row=1,
    has_headers=False,
)

assert headers == []
```

### 5.2. 不返回标题行

如果工作表有标题行，但调用方只关心数据，可以设置 `return_headers=False`。

```python
headers, rows_values = await client.sheets.query_values(
    spreadsheet_token="shtcn_xxx",
    sheet_id="sheet_xxx",
    start_row=2,
    has_headers=True,
    return_headers=False,
)

assert headers == []
```

`return_headers=False` 不会改变数据读取方式，只影响返回值中的 `headers`。

## 6. 接入 tabular 仓储

`AsyncLarkSheetsBackend` 实现了 `athena_kit.core.tabular.AsyncTableBackend`，可以把飞书工作表作为二维表格后端接入 `AsyncTableRepository`。

```python
from datetime import date

from athena_kit.core.tabular import AsyncTableRepository, TableCell, TableRow
from athena_kit.lark.sheets import AsyncLarkSheetsBackend, LarkSheetsLocator


class TradeRow(TableRow):
    trade_date: date = TableCell(title="日期", order=1)
    symbol: str = TableCell(title="代码", order=2)
    amount: int = TableCell(title="成交额", order=3)


async def main(client) -> None:
    backend = AsyncLarkSheetsBackend(client.sheets)
    locator = LarkSheetsLocator(
        spreadsheet_token="shtcn_xxx",
        sheet_id="sheet_xxx",
    )
    repository = AsyncTableRepository(backend, locator, TradeRow)

    await repository.replace_all([
        TradeRow(trade_date=date(2026, 6, 11), symbol="000001", amount=1200),
    ])

    rows = await repository.list_all()
```

如果飞书工作表没有标题行，但列顺序与 `TableRow.table_headers()` 一致，可以通过 `has_headers=False` 读取。

```python
rows = await repository.list_all(has_headers=False, start_row=1)
```

这时 repository 会使用模型定义中的 `TableCell(title=...)` 顺序作为列映射，而不会要求飞书表格返回标题行。

## 7. A1 notation 工具

Sheets 模块内置了 A1 notation 范围构造工具。大多数情况下不需要直接使用，因为 `overwrite_values()` 和 `query_values()` 会自动构造范围。需要手动构造范围时，可以使用：

```python
from athena_kit.lark.sheets.a1_notation import build_a1_range

cell_range = build_a1_range(
    sheet_id="sheet_xxx",
    n_rows=10,
    n_cols=3,
    start_row=2,
    start_col=1,
)

assert cell_range == "sheet_xxx!A2:C11"
```

## 8. 参考

- 飞书创建电子表格文档：https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet/create
- 飞书工作表操作：https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet-sheet/operate-sheets
- 飞书写入单个范围：https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/write-data-to-a-single-range
- 飞书读取单个范围：https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/reading-a-single-range
- HTTP 客户端说明：[athena_http.md](athena_http.md)
- Tabular 模型说明：[athena_tabular.md](athena_tabular.md)
