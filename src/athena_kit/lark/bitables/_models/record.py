from datetime import datetime
from typing import Any, NotRequired, TypedDict


class BitableRecord(TypedDict):
    """多维表格的一条记录。

    Attributes:
        record_id: 记录 ID。
        fields: 记录字段数据，不同字段类型的值结构不同。
        created_by: 创建人信息。
        created_time: 创建时间。
        last_modified_by: 最近修改人信息。
        last_modified_time: 最近修改时间。
    """

    record_id: str
    fields: dict[str, Any]
    created_by: NotRequired[dict[str, Any]]
    created_time: NotRequired[datetime]
    last_modified_by: NotRequired[dict[str, Any]]
    last_modified_time: NotRequired[datetime]
