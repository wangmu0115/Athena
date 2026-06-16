import httpx
from athena_kit.http.response_json import create_biz_code_validator, extract_response_json_values
from athena_kit.lark.drives.mapstruct import mapping_files
from athena_kit.lark.drives.requests import FetchFilesRequest
from athena_kit.lark.drives.responses import LarkFile

_DRIVE_SUCCESS_VALIDATOR = create_biz_code_validator(
    code_key="code",
    success_codes=(0,),
    message_key="msg",
)


class LarkDrivesAsyncClient:
    def __init__(self, aclient: httpx.AsyncClient):
        self._aclient = aclient

    async def list_files(self, folder_token: str) -> list[LarkFile]:
        """获取指定文件夹当前层级下的文件清单。为避免误读用户云空间根目录，本方法要求显式传入非空 `folder_token`。

        Args:
            folder_token: 文件夹 token，不支持空字符串。

        Returns:
            文件夹当前层级下的文件清单。

        Raises:
            ValueError: 当 `folder_token` 为空时抛出。

        References:
            https://open.feishu.cn/document/server-docs/docs/drive-v1/folder/list
        """
        if not folder_token:
            raise ValueError("`folder_token` should not be empty.")
        all_lark_files: list[LarkFile] = []
        request = FetchFilesRequest(folder_token=folder_token)
        while True:
            response = await self._aclient.get("/drive/v1/files", params=request.to_dict())
            has_more, next_page_token, raw_files = extract_response_json_values(
                response,
                ["data.has_more", "data.next_page_token", "data.files"],
                validator=_DRIVE_SUCCESS_VALIDATOR,
            )
            all_lark_files.extend(mapping_files(raw_files))

            if has_more and next_page_token:
                request.page_token = str(next_page_token)
            else:
                break

        return all_lark_files
