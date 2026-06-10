from typing import Any

import httpx
from athena_kit.http.hooks import (
    EventHooks,
    LoggingOptions,
    RequestIDOptions,
    ResponseStatusOptions,
    build_event_hooks,
)


class HttpClient(httpx.Client):
    """基于 `httpx.Client` 的同步 HTTP 客户端。

    该客户端只做很薄的一层封装，用于按需组装 Athena 内置的 event hooks，
    其余客户端参数、请求行为、超时、连接池、认证和异常模型都沿用 HTTPX。
    """

    def __init__(
        self,
        *args: Any,
        request_id: bool | RequestIDOptions = False,
        logging: bool | LoggingOptions = False,
        response_status: bool | ResponseStatusOptions = False,
        event_hooks: EventHooks | None = None,
        **kwargs: Any,
    ):
        super().__init__(
            *args,
            event_hooks=build_event_hooks(
                event_hooks,
                request_id=request_id,
                logging=logging,
                response_status=response_status,
            ),
            **kwargs,
        )
