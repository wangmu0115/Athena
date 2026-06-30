from typing import Any, NotRequired, TypedDict

from athena_kit.lark.bitables._models.enums import BitableFieldType, BitableFieldUiType


class BitableField(TypedDict):
    """多维表格字段的元数据。

    Attributes:
        field_id: 多维表格字段 ID。
        field_name: 多维表格字段名称。
        type: 多维表格字段类型，已知类型会映射为 `BitableFieldType`，未知的新类型会保留为原始 int。
        property: 字段属性，https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-table-field/guide#887ee1cd。
        is_primary: 是否索引列。
        is_hidden: 是否隐藏字段。
        ui_type: 字段在界面上的展示类型，已知类型会映射为 `BitableFieldUiType`，未知的新类型会保留为原始 str。
        description: 字段描述，当前请求按飞书默认行为返回，通常是字符串。
    """

    field_id: str
    field_name: str
    type: BitableFieldType | int
    property: dict[str, Any] | None
    is_primary: bool
    is_hidden: bool
    ui_type: BitableFieldUiType | str
    description: NotRequired[Any]
