from typing import Any, NotRequired, TypedDict


class BitableField(TypedDict):
    """多维表格字段的元数据。"""

    field_id: str
    field_name: str
    type: int
    property: dict[str, Any] | None
    is_primary: NotRequired[bool]
    ui_type: NotRequired[str]
    description: NotRequired[Any]
