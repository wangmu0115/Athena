from pydantic import Field

from athena_kit.lark._base import _BaseRequestModel


class FetchFilesRequest(_BaseRequestModel):
    folder_token: str = Field(..., description="文件夹的 token")

    page_size: int = Field(default=100, ge=1, le=200, description="每次返回的文件数量")
    page_token: str | None = Field(default=None, description="分页标记，第一次请求不填，表示从头开始遍历")
