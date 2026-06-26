import httpx
from athena_kit.http import create_biz_code_validator, extract_response_json_values
from athena_kit.lark.bitables.mappers import to_bitable_records
from athena_kit.lark.bitables.models import BitableRecord
from athena_kit.lark.bitables.requests import SearchBitableRecordsRequest

_BITABLE_SUCCESS_VALIDATOR = create_biz_code_validator(
    code_key="code",
    success_codes=(0,),
    message_key="msg",
)


class LarkBitableRecordsAsyncClient:
    """飞书多维表格记录资源异步客户端。"""

    def __init__(self, aclient: httpx.AsyncClient):
        self._aclient = aclient

    async def search_records(
        self,
        app_token: str,
        table_id: str,
        *,
        view_id: str | None = None,
        field_names: list[str] | None = None,
        page_size: int = 200,
        limit: int | None = None,
    ) -> list[BitableRecord]:
        """查询多维表格记录，自动读取全部分页结果。"""
        if not app_token:
            raise ValueError("`app_token` should not be empty.")
        if not table_id:
            raise ValueError("`table_id` should not be empty.")
        if not 1 <= page_size <= 500:
            raise ValueError("`page_size` should be between 1 and 500.")
        if limit is not None and limit < 0:
            raise ValueError("`limit` must be greater than or equal to 0.")
        if limit == 0:
            return []

        url = f"/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"
        query_params: dict[str, int | str] = {"page_size": page_size}
        request = SearchBitableRecordsRequest(view_id=view_id, field_names=field_names)
        records: list[BitableRecord] = []

        while True:
            response = await self._aclient.post(url, params=query_params, json=request.to_dict())
            has_more, next_page_token, raw_records = extract_response_json_values(
                response,
                ["data.has_more", "data.page_token", "data.items"],
                validator=_BITABLE_SUCCESS_VALIDATOR,
            )
            records.extend(to_bitable_records(raw_records))

            if limit is not None and len(records) >= limit:
                break
            if has_more is not True or not isinstance(next_page_token, str) or not next_page_token:
                break
            query_params["page_token"] = next_page_token

        return records if limit is None else records[:limit]
