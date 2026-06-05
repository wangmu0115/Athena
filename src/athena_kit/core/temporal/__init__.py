from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.core.temporal.normalize import (
        normalize_datetime_timezone,
        resolve_date_boundary,
    )
    from athena_kit.core.temporal.predicates import (
        is_aware_datetime,
        is_naive_datetime,
    )
    from athena_kit.core.temporal.timezone import (
        coerce_timezone,
        get_default_timezone,
        get_timezone,
        reload_default_timezone,
        set_default_timezone,
        timezone_context,
    )
    from athena_kit.core.temporal.types import (
        DateBoundaryPolicy,
        DateOutputFormat,
        DateTimeOutputFormat,
        NaiveDateTimePolicy,
        TimeOutputFormat,
        TimestampUnit,
    )

__all__ = (
    "normalize_datetime_timezone",
    "resolve_date_boundary",
    "is_aware_datetime",
    "is_naive_datetime",
    "coerce_timezone",
    "get_default_timezone",
    "get_timezone",
    "reload_default_timezone",
    "set_default_timezone",
    "timezone_context",
    "DateBoundaryPolicy",
    "DateOutputFormat",
    "DateTimeOutputFormat",
    "NaiveDateTimePolicy",
    "TimeOutputFormat",
    "TimestampUnit",
)

_dynamic_imports = {
    "normalize_datetime_timezone": "normalize",
    "resolve_date_boundary": "normalize",
    "is_aware_datetime": "predicates",
    "is_naive_datetime": "predicates",
    "coerce_timezone": "timezone",
    "get_default_timezone": "timezone",
    "get_timezone": "timezone",
    "reload_default_timezone": "timezone",
    "set_default_timezone": "timezone",
    "timezone_context": "timezone",
    "DateBoundaryPolicy": "types",
    "DateOutputFormat": "types",
    "DateTimeOutputFormat": "types",
    "NaiveDateTimePolicy": "types",
    "TimeOutputFormat": "types",
    "TimestampUnit": "types",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
