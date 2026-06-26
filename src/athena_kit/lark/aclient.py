from typing import Any, Self

import httpx
from athena_kit.http import AsyncHttpClient
from athena_kit.http.hooks import AsyncEventHooks, LoggingOptions, RequestIDOptions, ResponseStatusOptions
from athena_kit.lark.auth import LarkTenantAccessTokenAuth
from athena_kit.lark.bitables import LarkBitablesAsyncClient
from athena_kit.lark.drives.aclient import LarkDrivesAsyncClient
from athena_kit.lark.sheets import LarkSheetsAsyncClient


class AsyncLarkClient:
    """飞书开放平台异步客户端。

    构建客户端时需要传入 `app_id`、`app_secret` 和可选的 `tenant_access_token_url`，
    客户端会自动创建 tenant_access_token 认证器。
    `request_id`、`logging`、`response_status` 和 `event_hooks` 会透传给 `AsyncHttpClient`，
    用于启用请求 ID、请求日志、HTTP 状态异常检查以及自定义 HTTPX event hooks。
    其他 HTTPX `AsyncClient` 支持的关键字参数可以通过 `**kwargs` 继续透传给底层客户端。

    如果需要完全接管认证流程，可以直接使用 `AsyncHttpClient` 或 HTTPX `AsyncClient` 构建底层客户端，
    再传给具体的 Lark 资源客户端。

    References:
        透传参数: https://www.python-httpx.org/api/#asyncclient
    """

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        tenant_access_token_url: str = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        *,
        base_url: str = "https://open.feishu.cn/open-apis",
        timeout: float | httpx.Timeout = 30.0,
        request_id: bool | RequestIDOptions = False,
        logging: bool | LoggingOptions = False,
        response_status: bool | ResponseStatusOptions = True,
        event_hooks: AsyncEventHooks | None = None,
        **kwargs: Any,
    ):
        if "auth" in kwargs:
            raise ValueError("AsyncLarkClient manages auth automatically. " \
                    "To customize authentication, use the lower-level Lark resource clients directly.")  # fmt: off

        self._aclient = AsyncHttpClient(
            base_url=base_url,
            timeout=timeout,
            auth=LarkTenantAccessTokenAuth(app_id, app_secret, tenant_access_token_url),
            request_id=request_id,
            logging=logging,
            response_status=response_status,
            event_hooks=event_hooks,
            **kwargs,
        )
        # 注册 sheets 资源异步客户端
        self.sheets = LarkSheetsAsyncClient(self._aclient)
        self.drives = LarkDrivesAsyncClient(self._aclient)
        self.bitables = LarkBitablesAsyncClient(self._aclient)

    async def __aenter__(self) -> Self:
        await self._aclient.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._aclient.__aexit__(exc_type, exc, tb)

    async def aclose(self) -> None:
        await self._aclient.aclose()
