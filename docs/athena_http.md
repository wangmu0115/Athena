# athena http 使用指南

`athena_kit.http` 基于 [HTTPX](https://www.python-httpx.org/) 提供一组轻量工具。它不会重新实现一套 HTTP 客户端，而是在 HTTPX 的基础上补充 Athena 项目中常用的能力，包括同步/异步客户端封装、Event Hooks、JSON 响应解析和简单重试。

客户端本身只负责组装 Athena 内置 hooks，其余请求参数、认证、超时、连接池、代理、transport 和异常模型都沿用 HTTPX。因此，已经熟悉 HTTPX 的使用方可以继续按照 HTTPX 的方式传入 `base_url`、`timeout`、`headers`、`auth`、`limits` 等参数。

## 1. 安装

`athena-kit` 要求 Python 3.12 或更高版本。使用 HTTP 扩展时，需要安装 `http` extra，它会安装 HTTP 相关依赖。

```shell
uv add "athena-kit[http]"
```

如果项目已经安装了 `athena-kit`，也可以在依赖文件中补充 `http` extra，确保运行环境中包含 HTTPX 等 HTTP 能力所需依赖。

```shell
uv add "athena-kit[http]"
uv sync
```

安装后可以通过下面的方式确认 HTTP 模块可用：

```python
from athena_kit.http import AsyncHttpClient, HttpClient
```

## 2. 创建客户端

可以通过 `athena_kit.http.HttpClient` 创建同步客户端，也可以通过 `athena_kit.http.AsyncHttpClient` 创建异步客户端。它们分别继承自 `httpx.Client` 和 `httpx.AsyncClient`，所以大多数 HTTPX 客户端参数都可以直接透传。

建议优先使用上下文管理器创建客户端。这样可以复用连接池，并在退出作用域时自动关闭连接资源。

### 2.1. 同步客户端

同步场景可以使用 `HttpClient`。它适合脚本、同步 Web 框架、后台任务或暂时没有 async 运行环境的调用方。

```python
from athena_kit.http import HttpClient

with HttpClient(base_url="https://api.example.test", timeout=5.0) as client:
    response = client.get("/items", params={"page": 1})
    response.raise_for_status()
```

`HttpClient` 的请求方法和 HTTPX 一致，例如 `get`、`post`、`put`、`delete`。如果设置了 `base_url`，后续请求可以传入相对路径；如果没有设置 `base_url`，请求时需要传入完整 URL。

```python
from athena_kit.http import HttpClient

with HttpClient(headers={"User-Agent": "my-service"}) as client:
    response = client.post(
        "https://api.example.test/items",
        json={"name": "athena"},
    )
    response.raise_for_status()
```

### 2.2. 异步客户端

异步场景可以使用 `AsyncHttpClient`。它适合 async Web 框架、异步任务、并发请求或已经运行在 event loop 中的代码。

```python
from athena_kit.http import AsyncHttpClient


async def fetch_items() -> None:
    async with AsyncHttpClient(base_url="https://api.example.test", timeout=5.0) as client:
        response = await client.get("/items", params={"page": 1})
        response.raise_for_status()
```

异步客户端的请求方法需要使用 `await`。和同步客户端一样，它也支持 HTTPX 的常见配置项。

```python
from athena_kit.http import AsyncHttpClient


async def create_item() -> None:
    async with AsyncHttpClient(
        base_url="https://api.example.test",
        headers={"User-Agent": "my-service"},
        timeout=10.0,
    ) as client:
        response = await client.post("/items", json={"name": "athena"})
        response.raise_for_status()
```

## 3. Event Hooks

Event Hooks 用于在请求发送前或响应返回后执行额外逻辑。Athena 内置了请求 ID、日志和响应状态检查三个常用 hook，可以在创建客户端时通过布尔值快速启用，也可以传入对应的 Options 对象做细粒度配置。

如果你已经有 HTTPX 原生 event hooks，也可以继续通过 `event_hooks` 参数传入。Athena 会保留原有 hook 顺序，并在后面追加启用的内置 hooks。

### 3.1. 请求 ID

传入 `request_id=True` 可以自动为请求补充请求 ID。默认写入 `X-Request-ID`，如果请求已经包含该 header，则不会覆盖。

```python
from athena_kit.http import HttpClient

with HttpClient(base_url="https://api.example.test", request_id=True) as client:
    response = client.get("/items")
```

请求 ID 常用于日志串联、链路追踪和问题排查。需要自定义 header 名称或 ID 生成方式时，可以直接使用 hooks 包中的 `RequestIDOptions`。

```python
from athena_kit.http import HttpClient
from athena_kit.http.hooks import RequestIDOptions

with HttpClient(
    base_url="https://api.example.test",
    request_id=RequestIDOptions(header_name="X-Trace-ID"),
) as client:
    response = client.get("/items")
```

也可以自定义 `id_factory`，例如接入业务自己的 trace id 生成逻辑。

```python
from athena_kit.http import HttpClient
from athena_kit.http.hooks import RequestIDOptions


def create_trace_id() -> str:
    return "trace-from-current-context"


with HttpClient(
    base_url="https://api.example.test",
    request_id=RequestIDOptions(header_name="X-Trace-ID", id_factory=create_trace_id),
) as client:
    response = client.get("/items")
```

### 3.2. 日志

传入 `logging=True` 可以记录请求开始和响应完成日志。日志中会包含请求方法、URL、响应状态码和请求耗时。

```python
from athena_kit.http import HttpClient

with HttpClient(base_url="https://api.example.test", logging=True) as client:
    response = client.get("/items")
```

默认 logger 是 `logging.getLogger("athena_kit.http")`，默认日志级别是 `logging.INFO`。需要自定义 logger、日志级别、header 记录策略或敏感 header 时，可以使用 `LoggingOptions`。

```python
import logging
from athena_kit.http import HttpClient
from athena_kit.http.hooks import LoggingOptions

logger = logging.getLogger("my_service.http")

with HttpClient(
    base_url="https://api.example.test",
    logging=LoggingOptions(logger=logger, log_headers=True, sensitive_headers={"authorization"}),
) as client:
    response = client.get("/items")
```

`log_headers=True` 会记录请求头。涉及认证、Cookie、API Key 等敏感信息时，应通过 `sensitive_headers` 配置脱敏字段，避免把凭据写入日志。

### 3.3. 响应状态检查

传入 `response_status=True` 会在响应 hook 中检查 HTTP 状态码。默认会对 4xx/5xx 响应抛出 `httpx.HTTPStatusError`，不会因为重定向链中的 3xx 响应中断请求。

```python
import httpx
from athena_kit.http import HttpClient

try:
    with HttpClient(base_url="https://api.example.test", response_status=True) as client:
        response = client.get("/items")
except httpx.HTTPStatusError as exc:
    print(exc.response.status_code)
    print(exc.response.text)
```

如果某些状态码在业务上可以接受，可以使用 `ResponseStatusOptions.allowed_status_codes` 把它们加入白名单。

```python
from athena_kit.http import HttpClient
from athena_kit.http.hooks import ResponseStatusOptions

with HttpClient(
    base_url="https://api.example.test",
    response_status=ResponseStatusOptions(allowed_status_codes={200, 201, 202, 404}),
) as client:
    response = client.get("/items/unknown")
```

如果希望 3xx 重定向响应也触发 `response.raise_for_status()`，可以打开 `raise_on_redirects`。

```python
from athena_kit.http import HttpClient
from athena_kit.http.hooks import ResponseStatusOptions

with HttpClient(
    base_url="https://api.example.test",
    response_status=ResponseStatusOptions(raise_on_redirects=True),
) as client:
    response = client.get("/items")
```

### 3.4. 组合自定义 hooks

如果已经有 HTTPX 原生 event hooks，可以通过 `event_hooks` 传入。Athena 会以调用方提供的 hooks 作为起点，再追加启用的内置 hooks。

```python
import httpx
from athena_kit.http import HttpClient


def add_client_header(request: httpx.Request) -> None:
    request.headers["X-Client"] = "athena"


with HttpClient(
    base_url="https://api.example.test",
    event_hooks={"request": [add_client_header]},
    request_id=True,
    logging=True,
) as client:
    response = client.get("/items")
```

也可以直接使用 `athena_kit.http.hooks` 中的工厂方法，自己组装 HTTPX 客户端。这适合已经在项目中直接使用 `httpx.Client`，但又想复用 Athena hooks 的场景。

```python
import httpx
from athena_kit.http.hooks import build_event_hooks

with httpx.Client(
    base_url="https://api.example.test",
    event_hooks=build_event_hooks(request_id=True, logging=True, response_status=True),
) as client:
    response = client.get("/items")
```

异步场景可以使用 `build_async_event_hooks`。

```python
import httpx
from athena_kit.http.hooks import build_async_event_hooks

async with httpx.AsyncClient(
    base_url="https://api.example.test",
    event_hooks=build_async_event_hooks(request_id=True, logging=True, response_status=True),
) as client:
    response = await client.get("/items")
```

## 4. JSON 响应解析

HTTP 接口通常会返回 JSON，`athena_kit.http` 提供了一组 helper，用于解析响应 JSON、按路径提取字段，以及在提取前校验业务结构。

这些 helper 支持 JSON 顶层是对象、数组、字符串、数字、布尔值或 `None`。如果响应体不是合法 JSON，会抛出 `InvalidResponseJSONError`。

### 4.1. 解析完整 JSON

`parse_response_json` 会调用 `response.json()` 解析响应体，并把解析失败的异常统一转换为 `InvalidResponseJSONError`。

```python
from athena_kit.http import parse_response_json

value = parse_response_json(response)
```

当你只需要拿到完整 JSON 值，不需要路径提取或业务校验时，可以直接使用这个函数。

### 4.2. 提取单个值

`extract_response_json_value` 用于提取单个路径。当 `path=None` 时返回完整 JSON 值；当传入路径时，会从 JSON 中读取对应字段或数组元素。

```python
from athena_kit.http import extract_response_json_value

payload = extract_response_json_value(response)
first_item = extract_response_json_value(response, "data.items[0]")
```

字符串路径会按 `.` 拆分字段，并支持 `field[index]` 形式的数组下标。例如 `"data.items[0].id"` 会依次读取 `data`、`items`、第 0 个元素和 `id` 字段。

如果字段名本身包含 `.` 或 `[0]` 这类文本，请使用显式列表路径，由调用方明确每一层路径含义。

```python
from athena_kit.http import extract_response_json_value

value = extract_response_json_value(response, ["data.items[0]", "name"])
```

如果路径不存在或类型不匹配，默认返回 `None`。需要自定义默认值时，可以传入 `default`。

```python
from athena_kit.http import extract_response_json_value

name = extract_response_json_value(response, "data.name", default="")
```

### 4.3. 提取多个值

`extract_response_json_values` 用于一次提取多个路径。返回值是一个 tuple，顺序和 `paths` 参数一致。某个路径不存在或类型不匹配时，该位置返回 `None`。

```python
from athena_kit.http import extract_response_json_values

item_id, item_name = extract_response_json_values(response, ["data.items[0].id", "data.items[0].name"])
```

多值提取不提供统一 `default` 参数，因为不同路径通常有不同业务含义。需要不同默认值时，建议在调用后自行处理。

```python
item_id, item_name = extract_response_json_values(response, ["data.id", "data.name"])
item_name = item_name or ""
```

### 4.4. 业务结构校验

很多接口即使 HTTP 状态码是 200，也可能通过响应体中的业务字段表示失败。此时可以传入 `validator`，先校验完整 JSON 对象，再提取业务数据。

内置的 `create_biz_code_validator` 适合常见的业务状态码场景，例如响应体中包含 `code`、`message` 和 `data`。

```python
from athena_kit.http import create_biz_code_validator, extract_response_json_value

validator = create_biz_code_validator(code_key="code", success_codes=(0, "0"), message_key="message")

items = extract_response_json_value(response, "data.items", validator=validator)
```

也可以传入自定义校验函数。校验函数接收完整 JSON 对象，校验失败时抛出异常即可。建议抛出 `ResponseJSONValidationError`，这样调用方可以统一捕获 JSON 业务校验失败。

```python
from athena_kit.http import JSONObject, ResponseJSONValidationError, extract_response_json_value


def validate_payload(payload: JSONObject) -> None:
    if payload.get("ok") is not True:
        raise ResponseJSONValidationError("Response payload is not ok", payload=payload)


data = extract_response_json_value(response, "data", validator=validate_payload)
```

## 5. 重试

`athena_kit.http` 提供 `retry` 和 `retry_async` 两个轻量重试 helper。它们只负责重试循环、指数退避、jitter、结果判断、异常判断和可选日志记录；是否应该重试由调用方根据 HTTP 状态码、异常类型或业务异常自行决定。

如果需要熔断、全链路超时预算、before/after 回调、复杂统计或更强的策略组合，可以直接使用
[tenacity](https://tenacity.readthedocs.io/en/latest/) 或 [litl/backoff](https://github.com/litl/backoff) 等专门的重试库。

### 5.1. 同步重试

同步场景使用 `retry`。`request` 是一个无参 callable，通常用 `lambda` 或 `functools.partial` 把真正的请求和参数包起来。

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

`attempts` 表示最大尝试次数，包含第一次执行。比如 `attempts=3` 时，第一次执行不会等待；失败后等待 `initial_delay * multiplier**0` 再执行第二次；第二次失败后等待 `initial_delay * multiplier**1` 再执行第三次；第三次结束后直接返回或抛出异常。

如果请求参数需要动态传入，可以使用 `lambda` 或 `functools.partial` 包装成无参调用。

```python
from functools import partial
from athena_kit.http import retry

request = partial(client.get, "/items", params={"page": 1})
response = retry(request=request)
```

### 5.2. 异步重试

异步场景使用 `retry_async`。它的参数含义和 `retry` 一致，区别是 `request` 需要返回 awaitable。

```python
import httpx
from athena_kit.http import RetryOptions, retry_async

response = await retry_async(
    request=lambda: client.get("/items"),
    options=RetryOptions(attempts=3, initial_delay=0.2, multiplier=2.0, jitter=0.1, logger=True),
    should_retry_result=lambda response: response.status_code in {429, 500, 502, 503, 504},
    should_retry_exception=lambda exc: isinstance(exc, httpx.TimeoutException),
)
```

在 async 客户端中，`client.get("/items")` 本身会返回一个 awaitable，因此可以直接放进 `lambda` 中交给 `retry_async` 调用。

### 5.3. 业务失败重试

业务校验失败也可以作为重试条件。常见做法是让请求函数在校验失败时抛出 `ResponseJSONValidationError`，然后在 `should_retry_exception` 中判断该异常是否需要重试。

```python
from athena_kit.http import (
    ResponseJSONValidationError,
    create_biz_code_validator,
    extract_response_json_value,
    retry_async,
)

validator = create_biz_code_validator(code_key="code", success_codes=(0,))


async def request_items() -> object:
    response = await client.get("/items")
    return extract_response_json_value(response, "data.items", validator=validator)


items = await retry_async(
    request=request_items,
    should_retry_exception=lambda exc: isinstance(exc, ResponseJSONValidationError),
)
```

这种方式可以把 HTTP 传输失败、HTTP 状态码失败和业务结构失败放到同一个重试框架里处理。不过是否重试仍然建议由调用方显式声明，避免把不可恢复的业务失败也反复重试。
