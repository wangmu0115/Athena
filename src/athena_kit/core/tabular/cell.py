from typing import Any

from pydantic import Field
from pydantic.fields import FieldInfo


def TableCell(
    *,
    title: str | None = None,
    order: int = 0,
    **kwargs: Any,
) -> FieldInfo:
    """创建带有二维表格单元格元信息的 Pydantic 字段。

    `TableCell` 描述一行模型中的一个单元格，支持配置写入表格时使用的标题和列顺序。
    """
    extra = kwargs.pop("json_schema_extra", {}) or {}
    extra.update({
        "title": title,
        "order": order,
    })
    return Field(json_schema_extra=extra, **kwargs)
