from collections.abc import Callable
from typing import Any

from pydantic import Field
from pydantic.fields import FieldInfo


def TableField(
    *,
    title: str | None = None,
    order: int = 0,
    source: str | list[str] | tuple[str, ...] | None = None,
    required: bool = False,
    transform: Callable[[Any], Any] | None = None,
    **kwargs: Any,
) -> FieldInfo:
    """Create a Pydantic field with tabular metadata."""
    extra = kwargs.pop("json_schema_extra", {}) or {}
    extra.update({
        "title": title,
        "order": order,
        "source": source,
        "required": required,
        "transform": transform,
    })
    return Field(json_schema_extra=extra, **kwargs)


def SourceField(
    *,
    source: str | list[str] | tuple[str, ...] | None = None,
    required: bool = False,
    transform: Callable[[Any], Any] | None = None,
    **kwargs: Any,
) -> FieldInfo:
    """Backward-compatible alias for source mapping metadata."""
    return TableField(source=source, required=required, transform=transform, **kwargs)
