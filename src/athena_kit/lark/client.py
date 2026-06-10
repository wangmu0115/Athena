from typing import Self

from athena_kit.http import AsyncHttpClient
from athena_kit.lark.auth import LarkTenantAccessTokenAuth, LarkTenantTokenOptions
from athena_kit.lark.sheet import LarkSheetClient


class LarkClient:
    """Unified Lark Open Platform client."""

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        *,
        base_url: str = "https://open.feishu.cn/open-apis",
        timeout: float = 30.0,
        auth: LarkTenantAccessTokenAuth | None = None,
    ):
        self._aclient = AsyncHttpClient(
            base_url=base_url,
            timeout=timeout,
            auth=auth or LarkTenantAccessTokenAuth(LarkTenantTokenOptions.default(app_id, app_secret)),
        )
        self.sheets = LarkSheetClient(self._aclient)

    async def __aenter__(self) -> Self:
        await self._aclient.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._aclient.__aexit__(exc_type, exc, tb)
