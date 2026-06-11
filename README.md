# Athena Kit

Athena Kit 是 Athena 项目使用的模块化 Python 工具包。

它发布为一个 Python 包：`athena-kit`，并提供统一的 Python 命名空间：`athena_kit`。

## 安装

```shell
uv add athena-kit
uv add "athena-kit[http]"
uv add "athena-kit[lark]"
uv add "athena-kit[matplotlib]"
uv add "athena-kit[dataframe]"
uv add "athena-kit[all]"
```

## Usage

### athena http

`athena_kit.http` 基于 HTTPX 做薄封装，提供同步/异步客户端、常用 event hooks、JSON 响应提取和简单重试工具。

同步请求：

```python
from athena_kit.http import HttpClient

with HttpClient(base_url="https://api.example.test", request_id=True) as client:
    response = client.get("/items")
    response.raise_for_status()
```

异步请求：

```python
from athena_kit.http import AsyncHttpClient

async with AsyncHttpClient(base_url="https://api.example.test", request_id=True) as client:
    response = await client.get("/items")
    response.raise_for_status()
```

启用请求 ID、日志和响应状态检查：

```python
from athena_kit.http import HttpClient

with HttpClient(
    base_url="https://api.example.test",
    request_id=True,
    logging=True,
    response_status=True,
) as client:
    response = client.get("/items")
```

提取 JSON 响应中的业务数据：

```python
from athena_kit.http import create_biz_code_validator, extract_response_json_value

data = extract_response_json_value(
    response,
    "data.items[0]",
    validator=create_biz_code_validator(code_key="code", success_codes=(0,)),
)
```

为请求增加简单重试：

```python
import httpx
from athena_kit.http import RetryOptions, retry

response = retry(
    request=lambda: client.get("/items"),
    options=RetryOptions(attempts=3, initial_delay=0.2, multiplier=2.0, jitter=0.1, logger=True),
    should_retry_result=lambda response: response.status_code in {429, 500, 502, 503, 504},
    should_retry_exception=lambda exc: isinstance(exc, httpx.TimeoutException),
)
```

更多 HTTP 使用案例见 [docs/athena_http.md](docs/athena_http.md)。

### athena tabular

`athena_kit.core.tabular` 提供二维表格模型、单元格序列化、pandas DataFrame 转换，以及同步/异步表格后端和仓储抽象。

定义一行表格模型：

```python
from datetime import date

from athena_kit.core.tabular import TableCell, TableRow


class TradeRow(TableRow):
    trade_date: date = TableCell(title="日期", order=1)
    symbol: str = TableCell(title="代码", order=2)
    amount: int = TableCell(title="成交额", order=3)
```

模型和二维表格行互相转换：

```python
row = TradeRow(trade_date=date(2026, 6, 11), symbol="000001", amount=1200)

assert TradeRow.table_headers() == ["日期", "代码", "成交额"]
assert row.to_table_row() == ["2026-06-11", "000001", 1200]
```

使用 repository 接入具体二维表格后端：

```python
from athena_kit.core.tabular import TableRepository

repository = TableRepository(backend, locator, TradeRow)
rows = repository.list_all()
```

更多 Tabular 使用案例见 [docs/athena_tabular.md](docs/athena_tabular.md)。

### athena lark

`athena_kit.lark` 提供飞书开放平台异步客户端。当前重点支持 Sheets，包括创建电子表格、批量新增工作表、读写单个工作表范围，以及接入 `core.tabular` 的异步表格后端。

创建飞书客户端并新增电子表格：

```python
from athena_kit.lark import AsyncLarkClient


async with AsyncLarkClient(app_id="cli_xxx", app_secret="xxx", response_status=True) as client:
    spreadsheet_token, url = await client.sheets.create_spreadsheet(
        folder_token="fldcn_xxx",
        title="交易汇总",
    )
```

写入飞书工作表：

```python
revision, updated_rows, updated_columns = await client.sheets.overwrite_values(
    spreadsheet_token=spreadsheet_token,
    sheet_id="sheet_xxx",
    headers=["日期", "代码", "成交额"],
    rows_values=[["2026-06-11", "000001", 1200]],
    start_row=1,
)
```

接入异步表格仓储：

```python
from athena_kit.core.tabular import AsyncTableRepository
from athena_kit.lark.sheets import AsyncLarkSheetsBackend, LarkSheetsLocator

backend = AsyncLarkSheetsBackend(client.sheets)
locator = LarkSheetsLocator(spreadsheet_token=spreadsheet_token, sheet_id="sheet_xxx")
repository = AsyncTableRepository(backend, locator, TradeRow)

rows = await repository.list_all()
```

更多 Lark Sheets 使用案例见 [docs/athena_lark.md](docs/athena_lark.md)。

## 模块结构

- `athena_kit.core`：基础模型、时间编解码、表格和通用值处理工具。
- `athena_kit.http`：基于 HTTPX 的同步/异步 HTTP 工具。
- `athena_kit.lark`：飞书开放平台异步客户端和 Sheets 工具。
- `athena_kit.matplotlib`：声明式图表渲染工具。
- `athena_kit.bosun`：Bosun 表达式解析和 OpenTSDB 查询工具。

## 开发

```shell
uv sync --extra all
uv run ruff check src tests examples
uv run ruff format --check src tests examples
uv run pytest tests
```
