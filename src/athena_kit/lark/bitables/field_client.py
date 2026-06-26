import httpx
from athena_kit.http import create_biz_code_validator, extract_response_json_values
from athena_kit.lark.bitables.mappers import to_bitable_fields
from athena_kit.lark.bitables.models import BitableField

_BITABLE_SUCCESS_VALIDATOR = create_biz_code_validator(
    code_key="code",
    success_codes=(0,),
    message_key="msg",
)


class LarkBitableFieldsAsyncClient:
    """飞书多维表格字段资源异步客户端。"""

    def __init__(self, aclient: httpx.AsyncClient):
        self._aclient = aclient

    async def list_fields(
        self,
        app_token: str,
        table_id: str,
        *,
        view_id: str | None = None,
        text_field_as_array: bool = False,
        page_size: int = 100,
    ) -> list[BitableField]:
        """列出数据表中的全部字段元数据，并自动读取全部分页结果。

        References:
            https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-table-field/list
        """
        if not app_token:
            raise ValueError("`app_token` should not be empty.")
        if not table_id:
            raise ValueError("`table_id` should not be empty.")
        if not 1 <= page_size <= 100:
            raise ValueError("`page_size` should be between 1 and 100.")

        query_params: dict[str, int | str | bool] = {"page_size": page_size}
        if view_id is not None:
            query_params["view_id"] = view_id
        if text_field_as_array:
            query_params["text_field_as_array"] = True

        fields: list[BitableField] = []
        url = f"/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        while True:
            response = await self._aclient.get(url, params=query_params)
            has_more, next_page_token, raw_fields = extract_response_json_values(
                response,
                ["data.has_more", "data.page_token", "data.items"],
                validator=_BITABLE_SUCCESS_VALIDATOR,
            )
            fields.extend(to_bitable_fields(raw_fields))

            if has_more is not True or not isinstance(next_page_token, str) or not next_page_token:
                break
            query_params["page_token"] = next_page_token

        return fields
