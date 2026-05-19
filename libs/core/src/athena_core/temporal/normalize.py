from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from athena_core.temporal.predicates import is_aware_datetime
from athena_core.temporal.timezone import coerce_timezone, get_timezone
from athena_core.temporal.types import DateBoundaryPolicy
from athena_core.values.optional import optional_or_else


def resolve_date_boundary(d: date, tz: ZoneInfo, *, boundary_policy: DateBoundaryPolicy) -> datetime:
    """根据指定的日期边界策略，将 `date` 解析为带有时区信息的 `datetime`。"""
    match boundary_policy:
        case "start":
            return datetime.combine(d, time.min, tzinfo=tz)
        case "end":
            return datetime.combine(d, time.max, tzinfo=tz)
        case "noon":
            return datetime.combine(d, time(12, 0, 0), tzinfo=tz)
        case _:
            raise ValueError(f"Unsupported date_boundary_policy: {boundary_policy}")


def normalize_datetime_timezone(dt: datetime, *, tz: str | ZoneInfo | None = None) -> datetime:
    """将 `datetime` 归一化到目标时区。

    - 如果 `dt` 是 naive datetime，则会被视为已经属于目标时区，并直接附加目标时区信息。
    - 如果 `dt` 是 aware datetime，则会被转换到目标时区。
    """
    target_tz = coerce_timezone(optional_or_else(tz, default_factory=get_timezone))
    if is_aware_datetime(dt):
        return dt.astimezone(target_tz)
    return dt.replace(tzinfo=target_tz)
