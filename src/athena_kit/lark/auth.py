import asyncio
from datetime import datetime, timedelta

import httpx
from athena_kit.http import create_biz_code_validator, extract_response_json_values


class LarkTenantAccessTokenAuth(httpx.Auth):
    """用于 HTTPX 异步客户端的飞书 tenant_access_token 认证器。

    每次请求发送前，HTTPX 会调用 `async_auth_flow`。认证器会自动获取并缓存 tenant_access_token，
    在缓存过期前复用已有 token，并为请求补充 Authorization 与 Content-Type 请求头。

    构建该 Auth 需要传入飞书应用凭据 `app_id` 和 `app_secret`。
    `tenant_access_token_url` 是获取 tenant_access_token 的接口地址，可用于切换不同环境或兼容私有化部署。
    `refresh_before_expire` 表示在 token 过期前多少秒主动刷新。
    `timeout` 只作用于获取 tenant_access_token 的内部 HTTP 请求，不影响业务 API 请求的超时配置。

    References:
        https://open.feishu.cn/document/server-docs/authentication-management/access-token/tenant_access_token_internal
    """

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        tenant_access_token_url: str = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        *,
        refresh_before_expire: int = 300,
        timeout: float = 5.0,
    ):
        self._app_id = app_id
        self._app_secret = app_secret
        self._tenant_access_token_url = tenant_access_token_url
        self._refresh_before_expire = refresh_before_expire
        self._timeout = timeout
        self._token: str | None = None
        self._expire_at: datetime | None = None
        self._lock = asyncio.Lock()

    async def async_auth_flow(self, request: httpx.Request):
        token = await self.get_tenant_access_token()
        request.headers.setdefault("Authorization", f"Bearer {token}")
        request.headers.setdefault("Content-Type", "application/json;charset=utf-8")
        yield request

    async def get_tenant_access_token(self) -> str:
        if self._is_token_valid():
            assert self._token is not None  # 类型收窄提示
            return self._token

        async with self._lock:
            if self._is_token_valid():
                assert self._token is not None
                return self._token

            token, expire_at = await self._fetch_tenant_access_token()
            self._token = token
            self._expire_at = expire_at
            return token

    def _is_token_valid(self) -> bool:
        if not self._token or not self._expire_at:
            return False
        return self._expire_at > datetime.now()

    async def _fetch_tenant_access_token(self) -> tuple[str, datetime]:
        now = datetime.now()
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                self._tenant_access_token_url,
                json={"app_id": self._app_id, "app_secret": self._app_secret},
            )
        response.raise_for_status()

        tenant_access_token, expire = extract_response_json_values(
            response,
            ["tenant_access_token", "expire"],
            validator=create_biz_code_validator(
                code_key="code",
                success_codes=(0,),
                message_key="msg",
            ),
        )
        if not isinstance(tenant_access_token, str):
            raise TypeError("tenant_access_token should be a string.")
        if not isinstance(expire, int):
            raise TypeError("expire should be an integer.")

        expire_at = now + timedelta(seconds=max(expire - self._refresh_before_expire, 60))
        return tenant_access_token, expire_at
