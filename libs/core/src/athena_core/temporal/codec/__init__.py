from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_core.temporal.codec.date import (
        DateCodec,
        DateInput,
        DateOutput,
        format_date,
        parse_date,
    )
    from athena_core.temporal.codec.datetime import (
        DateTimeCodec,
        DateTimeInput,
        DateTimeOutput,
        format_datetime,
        parse_datetime,
    )
    from athena_core.temporal.codec.options import (
        DateCodecOptions,
        DateTimeCodecOptions,
        TemporalCodecOptions,
        TimeCodecOptions,
    )
    from athena_core.temporal.codec.temporal import TemporalCodec
    from athena_core.temporal.codec.time import (
        TimeCodec,
        TimeInput,
        TimeOutput,
        format_time,
        parse_time,
    )

__all__ = (
    "TemporalCodec",
    "DateCodec",
    "DateInput",
    "DateOutput",
    "format_date",
    "parse_date",
    "DateTimeCodec",
    "DateTimeInput",
    "DateTimeOutput",
    "format_datetime",
    "parse_datetime",
    "TimeCodec",
    "TimeInput",
    "TimeOutput",
    "format_time",
    "parse_time",
    "DateCodecOptions",
    "DateTimeCodecOptions",
    "TimeCodecOptions",
    "TemporalCodecOptions",
)

_dynamic_imports = {
    "TemporalCodec": "temporal",
    "DateCodec": "date",
    "DateInput": "date",
    "DateOutput": "date",
    "format_date": "date",
    "parse_date": "date",
    "DateTimeCodec": "datetime",
    "DateTimeInput": "datetime",
    "DateTimeOutput": "datetime",
    "format_datetime": "datetime",
    "parse_datetime": "datetime",
    "TimeCodec": "time",
    "TimeInput": "time",
    "TimeOutput": "time",
    "format_time": "time",
    "parse_time": "time",
    "DateCodecOptions": "options",
    "DateTimeCodecOptions": "options",
    "TimeCodecOptions": "options",
    "TemporalCodecOptions": "options",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
