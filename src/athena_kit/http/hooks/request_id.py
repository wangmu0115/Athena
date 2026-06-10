import uuid
from collections.abc import Callable
from dataclasses import dataclass

import httpx
from athena_kit.http.hooks.types import AsyncRequestHook, RequestHook


@dataclass(slots=True)
class RequestIDOptions:
    """请求 ID event hook 配置项。

    Attributes:
        header_name: 请求 ID 使用的 HTTP 头名称，默认是 `X-Request-ID`。
        id_factory: 每次需要补充请求 ID 时调用的无参函数，返回值会作为请求 ID 写入请求头。默认实现使用
            `uuid.uuid4()` 生成随机 UUID 字符串。只有请求中缺少 `header_name` 时才会调用该函数。
    """

    header_name: str = "X-Request-ID"
    id_factory: Callable[[], str] = lambda: str(uuid.uuid4())


def create_request_id_hook(options: RequestIDOptions | None = None) -> RequestHook:
    """创建同步 HTTPX request hook，用于为请求补充请求 ID。

    Args:
        options: 请求 ID hook 配置项，传入 `None` 时使用 `RequestIDOptions` 默认值。
    """
    options = options or RequestIDOptions()

    def add_request_id(request: httpx.Request) -> None:
        request.headers.setdefault(options.header_name, options.id_factory())

    return add_request_id


def create_async_request_id_hook(options: RequestIDOptions | None = None) -> AsyncRequestHook:
    """创建异步 HTTPX request hook，用于为请求补充请求 ID。

    Args:
        options: 请求 ID hook 配置项，传入 `None` 时使用 `RequestIDOptions` 默认值。
    """
    options = options or RequestIDOptions()

    async def add_request_id(request: httpx.Request) -> None:
        request.headers.setdefault(options.header_name, options.id_factory())

    return add_request_id
