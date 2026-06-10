import logging
import time
from collections.abc import Collection
from dataclasses import dataclass

import httpx
from athena_kit.http.hooks.types import (
    AsyncRequestHook,
    AsyncResponseHook,
    RequestHook,
    ResponseHook,
)

_START_TIME_KEY = "athena_kit.http.start_time"
_DEFAULT_LOGGER_NAME = "athena_kit.http"


@dataclass(slots=True)
class LoggingOptions:
    """HTTP 请求日志 event hook 的配置项，用于生成 request/response hook。

    - request hook: 在发送请求前记录请求开始信息，并把开始时间写入 `request.extensions`。
    - response hook: 在收到响应后读取开始时间，计算耗时并记录请求完成信息。

    Attributes:
        logger: 用于输出日志的 `logging.Logger`，传入 `None` 时使用 `logging.getLogger("athena_kit.http")`。
        level: 日志级别，默认是 `logging.INFO`。
        log_headers: 是否记录请求头。默认不记录，启用后会输出请求头，并对 `sensitive_headers` 中定义的请求头做脱敏。
        sensitive_headers: 需要脱敏的请求头名称集合，匹配时忽略大小写，默认包含认证凭据、Cookie、API Key 等敏感头。
    """

    logger: logging.Logger | None = None
    level: int = logging.INFO
    log_headers: bool = False
    sensitive_headers: Collection[str] = frozenset({"authorization", "cookie", "set-cookie", "x-api-key"})


def create_logging_hooks(options: LoggingOptions | None = None) -> tuple[RequestHook, ResponseHook]:
    """创建同步 HTTPX request/response hook，用于记录请求开始、响应完成和耗时。

    Args:
        options: 日志 hook 配置项，传入 `None` 时使用 `LoggingOptions` 默认值。
    """
    options = options or LoggingOptions()
    logger = options.logger or logging.getLogger(_DEFAULT_LOGGER_NAME)

    def log_request(request: httpx.Request) -> None:
        _log_request(logger, options, request)

    def log_response(response: httpx.Response) -> None:
        _log_response(logger, options, response)

    return log_request, log_response


def create_async_logging_hooks(options: LoggingOptions | None = None) -> tuple[AsyncRequestHook, AsyncResponseHook]:
    """创建异步 HTTPX request/response hook，用于记录请求开始、响应完成和耗时。

    Args:
        options: 日志 hook 配置项，传入 `None` 时使用 `LoggingOptions` 默认值。
    """
    options = options or LoggingOptions()
    logger = options.logger or logging.getLogger(_DEFAULT_LOGGER_NAME)

    async def log_request(request: httpx.Request) -> None:
        _log_request(logger, options, request)

    async def log_response(response: httpx.Response) -> None:
        _log_response(logger, options, response)

    return log_request, log_response


def _log_request(logger: logging.Logger, options: LoggingOptions, request: httpx.Request) -> None:
    request.extensions[_START_TIME_KEY] = time.perf_counter()
    headers: dict[str, str] | None = None
    if options.log_headers:
        headers = {}
        sensitive_headers = {header.lower() for header in options.sensitive_headers}
        for key, value in request.headers.items():
            normalized_value = "******" if key.lower() in sensitive_headers else value
            headers[key] = normalized_value

    logger.log(
        options.level,
        "HTTP request started: method=%s url=%s headers=%s",
        request.method,
        request.url,
        headers,
    )


def _log_response(logger: logging.Logger, options: LoggingOptions, response: httpx.Response) -> None:
    start_time = response.request.extensions.get(_START_TIME_KEY)
    elapsed_ms = None
    if isinstance(start_time, float):
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    logger.log(
        options.level,
        "HTTP request completed: method=%s url=%s status_code=%s elapsed_ms=%s",
        response.request.method,
        response.request.url,
        response.status_code,
        None if elapsed_ms is None else round(elapsed_ms, 2),
    )
