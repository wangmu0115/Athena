import httpx
from athena_kit.http import create_biz_code_validator, extract_response_json_values
from athena_kit.lark.bitables.fields.mappers import to_bitable_fields
from athena_kit.lark.bitables.models import BitableField

_BITABLE_SUCCESS_VALIDATOR = create_biz_code_validator(
    code_key="code",
    success_codes=(0,),
    message_key="msg",
)


class LarkBitableFieldsAsyncClient:
    def __init__(self, aclient: httpx.AsyncClient):
        self._aclient = aclient

    async def get_table_fields(
        self,
        app_token: str,
        table_id: str,
        *,
        view_id: str | None = None,
    ) -> list[BitableField]:
        """获取多维表格数据表中的的所有字段。

        Args:
            app_token: 多维表格 App 的唯一标识。
            table_id: 多维表格数据表的唯一标识。
            view_id: 可选的视图唯一标识，传入时仅返回该视图可见的字段。

        References:
            https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-table-field/list
        """
        if not app_token:
            raise ValueError("`app_token` should not be empty.")
        if not table_id:
            raise ValueError("`table_id` should not be empty.")

        query_params: dict[str, int | str] = {"page_size": 50}
        if view_id is not None:
            query_params["view_id"] = view_id

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
