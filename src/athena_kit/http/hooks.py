"""HTTPX event hook helpers for Athena HTTP clients.

References:
    HTTPX Event Hooks: https://www.python-httpx.org/advanced/event-hooks/
    HTTPX Exceptions: https://www.python-httpx.org/exceptions/
"""

import logging
import time
import uuid
from collections.abc import Awaitable, Callable, Collection, Sequence
from dataclasses import dataclass
from typing import TypedDict

import httpx

type AsyncRequestHook = Callable[[httpx.Request], Awaitable[None]]
type AsyncResponseHook = Callable[[httpx.Response], Awaitable[None]]
type RequestHook = Callable[[httpx.Request], None]
type ResponseHook = Callable[[httpx.Response], None]


class EventHooks(TypedDict, total=False):
    request: Sequence[RequestHook]
    response: Sequence[ResponseHook]


class AsyncEventHooks(TypedDict, total=False):
    request: Sequence[AsyncRequestHook]
    response: Sequence[AsyncResponseHook]


@dataclass(slots=True)
class RequestIDOptions:
    """请求 ID event hook 的配置项。

    该配置用于 `create_request_id_hook` 和 `create_async_request_id_hook` 生成的 request hook。

    Attributes:
        header_name: 请求 ID 使用的 HTTP 头名称，默认是 `X-Request-ID`。
        id_factory: 每次需要补充请求 ID 时调用的无参函数，返回值会作为请求 ID 写入请求头。默认实现使用
            `uuid.uuid4()` 生成随机 UUID 字符串。只有请求中缺少 `header_name` 时才会调用该函数。
    """

    header_name: str = "X-Request-ID"
    id_factory: Callable[[], str] = lambda: str(uuid.uuid4())


@dataclass(slots=True)
class LoggingOptions:
    """HTTP 请求日志 event hook 的配置项。

    该配置用于 `create_logging_hooks` 和 `create_async_logging_hooks` 生成的 request/response hook。
    request hook 会在 HTTPX 发送请求前记录请求开始信息，并把开始时间写入 `request.extensions`。
    response hook 会在收到响应后读取开始时间，计算耗时并记录请求完成信息。

    Attributes:
        logger: 用于输出日志的 `logging.Logger`。传入 `None` 时使用 `logging.getLogger("athena_kit.http")`。
        level: 日志级别，默认是 `logging.INFO`。
        log_headers: 是否记录请求头。默认不记录；启用后会输出请求头，并对 `sensitive_headers` 中定义的请求头做脱敏。
        sensitive_headers: 需要脱敏的请求头名称集合，匹配时忽略大小写。默认包含认证凭据、Cookie、API Key 等敏感头。
    """

    logger: logging.Logger | None = None
    level: int = logging.INFO
    log_headers: bool = False
    sensitive_headers: Collection[str] = frozenset({"authorization", "cookie", "set-cookie", "x-api-key"})


def create_request_id_hook(options: RequestIDOptions | None = None) -> RequestHook:
    """创建同步 HTTPX request hook，用于为请求补充请求 ID。

    Args:
        options: 请求 ID 的配置项。传入 `None` 时使用 `RequestIDOptions` 的默认配置。

    Returns:
        可传给 `httpx.Client(event_hooks={"request": [...]})` 的同步 request hook。
    """
    resolved = options or RequestIDOptions()

    def add_request_id(request: httpx.Request) -> None:
        request.headers.setdefault(resolved.header_name, resolved.id_factory())

    return add_request_id


def create_async_request_id_hook(options: RequestIDOptions | None = None) -> AsyncRequestHook:
    """创建异步 HTTPX request hook，用于为请求补充请求 ID。

    Args:
        options: 请求 ID 的配置项。传入 `None` 时使用 `RequestIDOptions` 的默认配置。

    Returns:
        可传给 `httpx.AsyncClient(event_hooks={"request": [...]})` 的异步 request hook。
    """
    resolved = options or RequestIDOptions()

    async def add_request_id(request: httpx.Request) -> None:
        request.headers.setdefault(resolved.header_name, resolved.id_factory())

    return add_request_id


_START_TIME_KEY = "athena_kit.http.start_time"


def create_logging_hooks(options: LoggingOptions | None = None) -> tuple[RequestHook, ResponseHook]:
    """创建同步 HTTPX request/response hook，用于记录请求开始、响应完成和耗时。

    Args:
        options: 日志 event hook 的配置项。传入 `None` 时使用 `LoggingOptions` 的默认配置。

    Returns:
        二元组 `(request_hook, response_hook)`，可分别传给 `httpx.Client(event_hooks={"request": [...]})` 和
        `httpx.Client(event_hooks={"response": [...]})`。request hook 会记录请求方法、URL 和可选请求头，response hook
        会记录响应状态码和请求耗时。
    """
    resolved = options or LoggingOptions()
    logger = resolved.logger or logging.getLogger("athena_kit.http")

    def log_request(request: httpx.Request) -> None:
        request.extensions[_START_TIME_KEY] = time.perf_counter()
        headers = _mask_headers(request.headers, resolved.sensitive_headers) if resolved.log_headers else None
        logger.log(
            resolved.level,
            "HTTP request started: method=%s url=%s headers=%s",
            request.method,
            request.url,
            headers,
        )

    def log_response(response: httpx.Response) -> None:
        start_time = response.request.extensions.get(_START_TIME_KEY)
        elapsed_ms = None
        if isinstance(start_time, float):
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        logger.log(
            resolved.level,
            "HTTP request completed: method=%s url=%s status_code=%s elapsed_ms=%s",
            response.request.method,
            response.request.url,
            response.status_code,
            None if elapsed_ms is None else round(elapsed_ms, 2),
        )

    return log_request, log_response


def create_async_logging_hooks(options: LoggingOptions | None = None) -> tuple[AsyncRequestHook, AsyncResponseHook]:
    """创建异步 HTTPX request/response hook，用于记录请求开始、响应完成和耗时。

    Args:
        options: 日志 event hook 的配置项。传入 `None` 时使用 `LoggingOptions` 的默认配置。

    Returns:
        二元组 `(request_hook, response_hook)`，可分别传给 `httpx.AsyncClient(event_hooks={"request": [...]})` 和
        `httpx.AsyncClient(event_hooks={"response": [...]})`。request hook 会记录请求方法和 URL；response hook
        会记录响应状态码和请求耗时。
    """
    resolved = options or LoggingOptions()
    logger = resolved.logger or logging.getLogger("athena_kit.http")

    async def log_request(request: httpx.Request) -> None:
        request.extensions[_START_TIME_KEY] = time.perf_counter()
        headers = _mask_headers(request.headers, resolved.sensitive_headers) if resolved.log_headers else None
        logger.log(
            resolved.level,
            "HTTP request started: method=%s url=%s headers=%s",
            request.method,
            request.url,
            headers,
        )

    async def log_response(response: httpx.Response) -> None:
        start_time = response.request.extensions.get(_START_TIME_KEY)
        elapsed_ms = None
        if isinstance(start_time, float):
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        logger.log(
            resolved.level,
            "HTTP request completed: method=%s url=%s status_code=%s elapsed_ms=%s",
            response.request.method,
            response.request.url,
            response.status_code,
            None if elapsed_ms is None else round(elapsed_ms, 2),
        )

    return log_request, log_response


def raise_for_status_hook(response: httpx.Response) -> None:
    """Raise `httpx.HTTPStatusError` for non-2xx responses."""
    response.raise_for_status()


def merge_event_hooks(
    event_hooks: EventHooks | None = None,
    *,
    request_id: RequestIDOptions | None = None,
    logging_options: LoggingOptions | None = None,
    raise_for_status: bool = False,
) -> dict[str, list[RequestHook | ResponseHook]]:
    """Merge Athena's optional sync hooks with caller-provided HTTPX hooks."""
    request_hooks = list((event_hooks or {}).get("request", []))
    response_hooks = list((event_hooks or {}).get("response", []))

    if request_id is not None:
        request_hooks.append(create_request_id_hook(request_id))

    if logging_options is not None:
        log_request, log_response = create_logging_hooks(logging_options)
        request_hooks.append(log_request)
        response_hooks.append(log_response)

    if raise_for_status:
        response_hooks.append(raise_for_status_hook)

    return {
        "request": request_hooks,
        "response": response_hooks,
    }


async def async_raise_for_status_hook(response: httpx.Response) -> None:
    """Raise `httpx.HTTPStatusError` for non-2xx responses from an async hook."""
    response.raise_for_status()


def merge_async_event_hooks(
    event_hooks: AsyncEventHooks | None = None,
    *,
    request_id: RequestIDOptions | None = None,
    logging_options: LoggingOptions | None = None,
    raise_for_status: bool = False,
) -> dict[str, list[AsyncRequestHook | AsyncResponseHook]]:
    """Merge Athena's optional async hooks with caller-provided HTTPX hooks."""
    request_hooks = list((event_hooks or {}).get("request", []))
    response_hooks = list((event_hooks or {}).get("response", []))

    if request_id is not None:
        request_hooks.append(create_async_request_id_hook(request_id))

    if logging_options is not None:
        log_request, log_response = create_async_logging_hooks(logging_options)
        request_hooks.append(log_request)
        response_hooks.append(log_response)

    if raise_for_status:
        response_hooks.append(async_raise_for_status_hook)

    return {
        "request": request_hooks,
        "response": response_hooks,
    }


def _mask_headers(headers: httpx.Headers, sensitive_headers: Collection[str]) -> dict[str, str]:
    normalized_sensitive_headers = {header.lower() for header in sensitive_headers}
    return {key: "******" if key.lower() in normalized_sensitive_headers else value for key, value in headers.items()}
