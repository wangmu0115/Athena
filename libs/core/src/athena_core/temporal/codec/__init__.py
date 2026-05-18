from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_core.temporal.codec.datetime import (
        DateTimeCodec,
        format_datetime,
        parse_datetime,
    )

__all__ = (
    "DateTimeCodec",
    "format_datetime",
    "parse_datetime",
)

_dynamic_imports = {
    "DateTimeCodec": "datetime",
    "format_datetime": "datetime",
    "parse_datetime": "datetime",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
