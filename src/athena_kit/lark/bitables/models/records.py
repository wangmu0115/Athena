from typing import Any, NotRequired, TypedDict


class BitableRecord(TypedDict):
    """多维表格的一条记录。"""

    record_id: str
    fields: dict[str, Any]
    created_by: NotRequired[dict[str, Any]]
    created_time: NotRequired[int]
    last_modified_by: NotRequired[dict[str, Any]]
    last_modified_time: NotRequired[int]
