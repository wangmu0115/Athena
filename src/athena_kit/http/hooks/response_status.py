from collections.abc import Collection
from dataclasses import dataclass

import httpx
from athena_kit.http.hooks.types import AsyncResponseHook, ResponseHook


@dataclass(slots=True)
class ResponseStatusOptions:
    """HTTP status event hook 的配置项。

    默认行为只对 4xx/5xx 抛出 `httpx.HTTPStatusError`，避免在 HTTPX 处理重定向链时被 3xx 响应打断。

    Attributes:
        raise_on_redirects: 是否对 3xx 响应也调用 `response.raise_for_status()`，默认关闭。
        allowed_status_codes: 永远不抛异常的 HTTP 状态码集合，优先级高于 `raise_on_redirects`。
    """

    raise_on_redirects: bool = False
    allowed_status_codes: Collection[int] = frozenset()


def create_response_status_hook(options: ResponseStatusOptions | None = None) -> ResponseHook:
    """创建同步 HTTPX response hook，用于按配置检查响应状态。

    Args:
        options: 响应状态 hook 配置项，传入 `None` 时使用 `ResponseStatusOptions` 默认值。
    """
    options = options or ResponseStatusOptions()

    def check_response_status(response: httpx.Response) -> None:
        _check_response_status(response, options)

    return check_response_status


def create_async_response_status_hook(options: ResponseStatusOptions | None = None) -> AsyncResponseHook:
    """创建异步 HTTPX response hook，用于按配置检查响应状态。

    Args:
        options: 响应状态 hook 配置项，传入 `None` 时使用 `ResponseStatusOptions` 默认值。
    """
    options = options or ResponseStatusOptions()

    async def check_response_status(response: httpx.Response) -> None:
        _check_response_status(response, options)

    return check_response_status


def _check_response_status(response: httpx.Response, options: ResponseStatusOptions) -> None:
    if response.status_code in options.allowed_status_codes:
        return

    if 300 <= response.status_code < 400 and not options.raise_on_redirects:
        return

    response.raise_for_status()
