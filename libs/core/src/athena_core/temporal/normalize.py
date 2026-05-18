from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from athena_core.temporal.base import DateBoundaryPolicy


def resolve_date_boundary(d: date, tz: ZoneInfo, *, boundary_policy: DateBoundaryPolicy) -> datetime:
    """将 `date` 解析为具有时区的 `datetime`"""
    match boundary_policy:
        case "start":
            return datetime.combine(d, time.min, tzinfo=tz)
        case "end":
            return datetime.combine(d, time.max, tzinfo=tz)
        case "noon":
            return datetime.combine(d, time(12, 0, 0), tzinfo=tz)
        case _:
            raise ValueError(f"Unsupported date_boundary_policy: {boundary_policy}")
