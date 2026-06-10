import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Self

import httpx
from athena_kit.http import extract_response_json_values
from athena_kit.lark.validators import LARK_SUCCESS_VALIDATOR


@dataclass(slots=True)
class LarkTenantTokenOptions:
    app_id: str
    app_secret: str
    refresh_before_expire: int = 300
    timeout: float = 5.0
    token_url: str = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

    @classmethod
    def default(cls, app_id: str, app_secret: str) -> Self:
        return cls(app_id=app_id, app_secret=app_secret)


class LarkTenantAccessTokenAuth(httpx.Auth):
    """HTTPX auth implementation for Lark tenant access tokens."""

    def __init__(self, options: LarkTenantTokenOptions):
        self._options = options
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
            assert self._token is not None
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
        async with httpx.AsyncClient(timeout=self._options.timeout) as client:
            response = await client.post(
                self._options.token_url,
                json={
                    "app_id": self._options.app_id,
                    "app_secret": self._options.app_secret,
                },
            )
        response.raise_for_status()

        tenant_access_token, expire = extract_response_json_values(
            response,
            ["tenant_access_token", "expire"],
            validator=LARK_SUCCESS_VALIDATOR,
        )
        if not isinstance(tenant_access_token, str):
            raise TypeError("tenant_access_token should be a string.")
        if not isinstance(expire, int):
            raise TypeError("expire should be an integer.")

        expire_at = now + timedelta(seconds=max(expire - self._options.refresh_before_expire, 60))
        return tenant_access_token, expire_at
