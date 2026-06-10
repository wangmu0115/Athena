import asyncio
import logging
import random
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

import httpx

_DEFAULT_RETRY_LOGGER_NAME = "athena_kit.http.retry"


@dataclass(slots=True)
class RetryOptions:
    """重试配置。

    第一次执行不会等待，后续失败重试前等待时间采用指数退避 `initial_delay * multiplier**attempt`，最大等待时间
    不会超过 `max_delay`，当 `jitter > 0` 时，会额外追加 `[0, jitter]` 区间内的随机抖动，避免多个调用方同时重试。

    Attributes:
        attempts: 最大尝试次数，包含首次调用，默认 3 次，`attempts=1` 时，不会重试。
        initial_delay: 首次重试前等待秒数，默认 0.2 秒。
        max_delay: 单次等待的最大秒数，默认 5.0 秒。
        multiplier: 每次重试后等待时间的倍数，默认 2.0 倍。
        jitter: 每次等待额外增加的随机秒数上限，默认 0.1 秒，传入 `0` 时关闭 jitter。
        retry_exceptions: 默认可重试异常类型。
        logger: 是否记录重试日志。传入 `False` 时不记录；传入 `True` 时使用
            `logging.getLogger("athena_kit.http.retry")`；也可以传入自定义 `logging.Logger`。
        log_level: 重试日志级别，默认 `logging.WARNING`。
    """

    attempts: int = 3
    initial_delay: float = 0.2
    max_delay: float = 5.0
    multiplier: float = 2.0
    jitter: float = 0.1
    retry_exceptions: tuple[type[BaseException], ...] = (httpx.TimeoutException, httpx.TransportError)
    logger: logging.Logger | bool = False
    log_level: int = logging.WARNING


def retry[T](
    request: Callable[[], T],
    *,
    options: RetryOptions | None = None,
    should_retry_result: Callable[[T], bool] | None = None,
    should_retry_exception: Callable[[BaseException], bool] | None = None,
) -> T:
    """同步执行带重试的操作。

    Args:
        request: 需要执行的无参 HTTP 请求或请求相关操作。
        options: 重试配置，传入 `None` 时使用 `RetryOptions` 默认值。
        should_retry_result: 根据返回值判断是否重试的函数。返回 `True` 时会在剩余次数内重试。
        should_retry_exception: 根据异常判断是否重试的函数。传入 `None` 时使用 `options.retry_exceptions`。
    """
    options = options or RetryOptions()
    _validate_options(options)

    for attempt in range(options.attempts):
        try:
            result = request()
        except BaseException as exc:
            if attempt == options.attempts - 1 or not _should_retry_exception(exc, options, should_retry_exception):
                raise
            delay = _calculate_delay(options, attempt)
            _log_retry(options, attempt=attempt, delay=delay, reason="exception", detail=exc)
            time.sleep(delay)
            continue

        if attempt == options.attempts - 1 or should_retry_result is None or not should_retry_result(result):
            return result

        delay = _calculate_delay(options, attempt)
        _log_retry(options, attempt=attempt, delay=delay, reason="result", detail=result)
        time.sleep(delay)

    raise RuntimeError("Unreachable retry state")


async def retry_async[T](
    request: Callable[[], Awaitable[T]],
    *,
    options: RetryOptions | None = None,
    should_retry_result: Callable[[T], bool] | None = None,
    should_retry_exception: Callable[[BaseException], bool] | None = None,
) -> T:
    """异步执行带重试的操作。

    Args:
        request: 需要执行的无参异步 HTTP 请求或请求相关操作。
        options: 重试配置，传入 `None` 时使用 `RetryOptions` 默认值。
        should_retry_result: 根据返回值判断是否重试的函数。返回 `True` 时会在剩余次数内重试。
        should_retry_exception: 根据异常判断是否重试的函数。传入 `None` 时使用 `options.retry_exceptions`。
    """
    options = options or RetryOptions()
    _validate_options(options)

    for attempt in range(options.attempts):
        try:
            result = await request()
        except BaseException as exc:
            if attempt == options.attempts - 1 or not _should_retry_exception(exc, options, should_retry_exception):
                raise
            delay = _calculate_delay(options, attempt)
            _log_retry(options, attempt=attempt, delay=delay, reason="exception", detail=exc)
            await asyncio.sleep(delay)
            continue

        if attempt == options.attempts - 1 or should_retry_result is None or not should_retry_result(result):
            return result

        delay = _calculate_delay(options, attempt)
        _log_retry(options, attempt=attempt, delay=delay, reason="result", detail=result)
        await asyncio.sleep(delay)

    raise RuntimeError("Unreachable retry state")


def _should_retry_exception(
    exc: BaseException,
    options: RetryOptions,
    should_retry_exception: Callable[[BaseException], bool] | None,
) -> bool:
    if should_retry_exception is not None:
        return should_retry_exception(exc)

    return isinstance(exc, options.retry_exceptions)


def _calculate_delay(options: RetryOptions, attempt: int) -> float:
    """计算本次重试前的等待时间。

    等待时间使用指数退避：`initial_delay * multiplier**attempt`，并受 `max_delay` 限制。
    当 `jitter > 0` 时，会额外追加 `[0, jitter]` 区间内的随机抖动，避免多个调用方同时重试。
    """
    delay = min(options.initial_delay * (options.multiplier**attempt), options.max_delay)
    if options.jitter > 0:
        delay += random.uniform(0, options.jitter)
    return delay


def _log_retry(options: RetryOptions, *, attempt: int, delay: float, reason: str, detail: object) -> None:
    if options.logger is False:
        return
    logger = logging.getLogger(_DEFAULT_RETRY_LOGGER_NAME) if options.logger is True else options.logger

    logger.log(
        options.log_level,
        "Retrying HTTP request: retry=%s/%s delay=%.4fs reason=%s detail=%r",
        attempt + 1,
        options.attempts - 1,
        delay,
        reason,
        detail,
    )


def _validate_options(options: RetryOptions) -> None:
    if options.attempts < 1:
        raise ValueError("`attempts` should be greater than or equal to 1.")
    if options.initial_delay < 0:
        raise ValueError("`initial_delay` should be greater than or equal to 0.")
    if options.max_delay < 0:
        raise ValueError("`max_delay` should be greater than or equal to 0.")
    if options.multiplier < 1:
        raise ValueError("`multiplier` should be greater than or equal to 1.")
    if options.jitter < 0:
        raise ValueError("`jitter` should be greater than or equal to 0.")
