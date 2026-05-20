from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from athena_core.temporal.predicates import is_aware_datetime
from athena_core.temporal.timezone import coerce_timezone, get_timezone
from athena_core.temporal.types import DateBoundaryPolicy
from athena_core.values.optional import optional_or_else


def resolve_date_boundary(d: date, tz: ZoneInfo, *, boundary_policy: DateBoundaryPolicy) -> datetime:
    """将 `date` 按指定边界补全为带时区的 `datetime`。

    Args:
        d: 需要补全的日期。
        tz: 补全后 `datetime` 使用的时区。
        boundary_policy: 日期补全策略。

    Returns:
        带有 `tzinfo` 的 `datetime`。

    Raises:
        ValueError: 当 `boundary_policy` 不是受支持的取值时抛出。
    """
    match boundary_policy:
        case "start":
            return datetime.combine(d, time.min, tzinfo=tz)
        case "end":
            return datetime.combine(d, time(23, 59, 59), tzinfo=tz)
        case "end_max":
            return datetime.combine(d, time.max, tzinfo=tz)
        case "noon":
            return datetime.combine(d, time(12, 0, 0), tzinfo=tz)
        case _:
            raise ValueError(f"Unsupported date_boundary_policy: {boundary_policy}")


def normalize_datetime_timezone(dt: datetime, *, tz: str | ZoneInfo | None = None) -> datetime:
    """将 `datetime` 归一化到目标时区。

    如果 `dt` 是 aware datetime，会使用 `astimezone()` 转换到目标时区。
    如果 `dt` 是 naive datetime，会将其视为目标时区下的本地时间，并直接附加 `tzinfo`。

    Args:
        dt: 需要归一化的 `datetime`。
        tz: 目标时区。未传入时使用 `get_timezone()` 返回的当前有效时区。

    Returns:
        带有目标时区信息的 `datetime`。
    """
    target_tz = coerce_timezone(optional_or_else(tz, default_factory=get_timezone))
    if is_aware_datetime(dt):
        return dt.astimezone(target_tz)
    return dt.replace(tzinfo=target_tz)
