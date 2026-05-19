from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_core.temporal.codec.datetime import (
        DateTimeCodec,
        format_datetime,
        parse_datetime,
    )
    from athena_core.temporal.codec.time import (
        TimeCodec,
        TimeInput,
        TimeOutput,
        format_time,
        parse_time,
    )

__all__ = (
    "DateTimeCodec",
    "format_datetime",
    "parse_datetime",
    "TimeCodec",
    "TimeInput",
    "TimeOutput",
    "format_time",
    "parse_time",
)

_dynamic_imports = {
    "DateTimeCodec": "datetime",
    "format_datetime": "datetime",
    "parse_datetime": "datetime",
    "TimeCodec": "time",
    "TimeInput": "time",
    "TimeOutput": "time",
    "format_time": "time",
    "parse_time": "time",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
