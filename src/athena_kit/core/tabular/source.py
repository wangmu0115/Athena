from collections.abc import Callable
from typing import Any

from pydantic import Field
from pydantic.fields import FieldInfo


def SourceCell(
    *,
    source: str | list[str] | tuple[str, ...] | None = None,
    required: bool = False,
    transform: Callable[[Any], Any] | None = None,
    **kwargs: Any,
) -> FieldInfo:
    """创建带有外部来源映射元信息的 Pydantic 字段。

    `SourceCell` 描述外部数据结构的列如何映射到模型字段，例如 pandas DataFrame、CSV、飞书表格或数据库查询结果。
    它只表达“来源 -> 模型”的映射，不负责定义模型写入规范表格时的标题和列顺序。
    """
    extra = kwargs.pop("json_schema_extra", {}) or {}
    extra.update({
        "source": source,
        "required": required,
        "transform": transform,
    })
    return Field(json_schema_extra=extra, **kwargs)
