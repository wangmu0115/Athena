from collections.abc import Collection
from dataclasses import dataclass

import httpx
from athena_kit.http.hooks.types import AsyncResponseHook, ResponseHook


@dataclass(slots=True)
class RaiseForStatusOptions:
    """HTTP status event hook 的配置项。

    默认行为只对 4xx/5xx 抛出 `httpx.HTTPStatusError`，避免在 HTTPX 处理重定向链时被 3xx 响应打断。

    Attributes:
        raise_on_redirects: 是否对 3xx 响应也调用 `response.raise_for_status()`。默认关闭。
        allowed_status_codes: 永远不抛异常的 HTTP 状态码集合，优先级高于 `raise_on_redirects`。
    """

    raise_on_redirects: bool = False
    allowed_status_codes: Collection[int] = frozenset()


def create_raise_for_status_hook(options: RaiseForStatusOptions | None = None) -> ResponseHook:
    """创建同步 HTTPX response hook，用于按配置检查响应状态。"""
    options = options or RaiseForStatusOptions()

    def raise_for_status(response: httpx.Response) -> None:
        _raise_for_status(response, options)

    return raise_for_status


def create_async_raise_for_status_hook(options: RaiseForStatusOptions | None = None) -> AsyncResponseHook:
    """创建异步 HTTPX response hook，用于按配置检查响应状态。"""
    options = options or RaiseForStatusOptions()

    async def raise_for_status(response: httpx.Response) -> None:
        _raise_for_status(response, options)

    return raise_for_status


def raise_for_status_hook(response: httpx.Response) -> None:
    """Raise `httpx.HTTPStatusError` for 4xx/5xx responses."""
    _raise_for_status(response, RaiseForStatusOptions())


async def async_raise_for_status_hook(response: httpx.Response) -> None:
    """Raise `httpx.HTTPStatusError` for 4xx/5xx responses from an async hook."""
    _raise_for_status(response, RaiseForStatusOptions())


def _raise_for_status(response: httpx.Response, options: RaiseForStatusOptions) -> None:
    if response.status_code in options.allowed_status_codes:
        return

    if 300 <= response.status_code < 400 and not options.raise_on_redirects:
        return

    response.raise_for_status()
