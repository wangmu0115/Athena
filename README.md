# Athena Kit

Athena Kit 是 Athena 项目使用的模块化 Python 工具包。

它发布为一个 Python 包：`athena-kit`，并提供统一的 Python 命名空间：`athena_kit`。

## 安装

```shell
uv add athena-kit
uv add "athena-kit[http]"
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

## 模块结构

- `athena_kit.core`：基础模型、时间编解码、表格和通用值处理工具。
- `athena_kit.http`：基于 HTTPX 的同步/异步 HTTP 工具。
- `athena_kit.matplotlib`：声明式图表渲染工具。
- `athena_kit.bosun`：Bosun 表达式解析和 OpenTSDB 查询工具。

## 开发

```shell
uv sync --extra all
uv run ruff check src tests examples
uv run ruff format --check src tests examples
uv run pytest tests
```
