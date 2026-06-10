# athena http 使用指南

`athena_kit.http` 基于 HTTPX 提供一组轻量工具。客户端本身只负责组装 Athena 内置 hooks，其余请求参数、认证、超时、连接池、代理、transport 和异常模型都沿用 HTTPX。

## 安装

```shell
uv add "athena-kit[http]"
```

## 同步客户端

```python
from athena_kit.http import HttpClient

with HttpClient(base_url="https://api.example.test", timeout=5.0) as client:
    response = client.get("/items", params={"page": 1})
    response.raise_for_status()
```

## 异步客户端

```python
from athena_kit.http import AsyncHttpClient


async def fetch_items() -> None:
    async with AsyncHttpClient(base_url="https://api.example.test", timeout=5.0) as client:
        response = await client.get("/items", params={"page": 1})
        response.raise_for_status()
```

## 请求 ID

传入 `request_id=True` 可以自动为请求补充请求 ID。默认写入 `X-Request-ID`，如果请求已经包含该 header，则不会覆盖。

```python
from athena_kit.http import HttpClient

with HttpClient(base_url="https://api.example.test", request_id=True) as client:
    response = client.get("/items")
```

需要自定义 header 名称或 ID 生成方式时，可以直接使用 hooks 包中的配置：

```python
from athena_kit.http import HttpClient
from athena_kit.http.hooks import RequestIDOptions

with HttpClient(
    base_url="https://api.example.test",
    request_id=RequestIDOptions(header_name="X-Trace-ID"),
) as client:
    response = client.get("/items")
```

## 日志

传入 `logging=True` 可以记录请求和响应日志。

```python
from athena_kit.http import HttpClient

with HttpClient(base_url="https://api.example.test", logging=True) as client:
    response = client.get("/items")
```

需要自定义 logger、日志级别、header 记录策略或敏感 header 时，可以使用 `LoggingOptions`。

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

## 响应状态检查

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

需要把某些状态码视为成功时，可以使用 `ResponseStatusOptions`。

```python
from athena_kit.http import HttpClient
from athena_kit.http.hooks import ResponseStatusOptions

with HttpClient(
    base_url="https://api.example.test",
    response_status=ResponseStatusOptions(allowed_status_codes={200, 201, 202, 404}),
) as client:
    response = client.get("/items/unknown")
```

## 组合自定义 hooks

如果已经有 HTTPX 原生 event hooks，可以通过 `event_hooks` 传入。Athena 会保留原有 hook 顺序，并在后面追加启用的内置 hooks。

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

也可以直接使用 `athena_kit.http.hooks` 中的工厂方法，自己组装 HTTPX 客户端。

```python
import httpx
from athena_kit.http.hooks import build_event_hooks

with httpx.Client(
    base_url="https://api.example.test",
    event_hooks=build_event_hooks(request_id=True, logging=True, response_status=True),
) as client:
    response = client.get("/items")
```

## JSON 响应解析

`parse_response_json` 会解析响应体，并允许 JSON 顶层是对象、数组、字符串、数字、布尔值或 `null`。

```python
from athena_kit.http import parse_response_json

value = parse_response_json(response)
```

`extract_response_json_value` 用于提取单个路径；当 `path=None` 时返回完整 JSON 值。

```python
from athena_kit.http import extract_response_json_value

payload = extract_response_json_value(response)
first_item = extract_response_json_value(response, "data.items[0]")
```

字符串路径会按 `.` 拆分字段，并支持 `field[index]` 形式的数组下标。如果字段名本身包含 `.` 或 `[0]` 这类文本，请使用显式列表路径。

```python
from athena_kit.http import extract_response_json_value

value = extract_response_json_value(response, ["data.items[0]", "name"])
```

`extract_response_json_values` 用于一次提取多个路径。某个路径不存在或类型不匹配时，该位置返回 `None`。

```python
from athena_kit.http import extract_response_json_values

item_id, item_name = extract_response_json_values(response, ["data.items[0].id", "data.items[0].name"])
```

## 业务结构校验

如果接口返回结构需要先判断业务状态，可以传入 `validator`。内置的 `create_biz_code_validator` 适合常见的业务状态码场景。

```python
from athena_kit.http import create_biz_code_validator, extract_response_json_value

validator = create_biz_code_validator(code_key="code", success_codes=(0, "0"), message_key="message")

items = extract_response_json_value(response, "data.items", validator=validator)
```

也可以传入自定义校验函数。校验函数接收完整 JSON 对象，校验失败时抛出异常即可。

```python
from athena_kit.http import JSONObject, ResponseJSONValidationError, extract_response_json_value


def validate_payload(payload: JSONObject) -> None:
    if payload.get("ok") is not True:
        raise ResponseJSONValidationError("Response payload is not ok", payload=payload)


data = extract_response_json_value(response, "data", validator=validate_payload)
```

## 同步重试

`retry` 只提供轻量的重试循环、指数退避、jitter、结果判断和异常判断。是否重试由调用方根据响应状态码、异常类型或业务异常自行决定。

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

如果请求参数需要动态传入，可以使用 `lambda` 或 `functools.partial` 包装成无参调用。

```python
from functools import partial
from athena_kit.http import retry

request = partial(client.get, "/items", params={"page": 1})
response = retry(request=request)
```

## 异步重试

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

业务校验失败也可以作为重试条件：让请求函数在校验失败时抛出业务异常，然后在 `should_retry_exception` 中判断。

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

复杂重试策略，例如熔断、按异常分组统计、全链路超时预算或更复杂的 before/after 回调，可以直接使用 `tenacity` 等专门的重试库。
