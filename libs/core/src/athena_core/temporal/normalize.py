from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from athena_core.temporal.base import DateBoundaryPolicy


def convert_date_to_datetime(d: date, tz: ZoneInfo, *, policy: DateBoundaryPolicy) -> datetime:
    match policy:
        case "start":
            return datetime.combine(d, time.min, tzinfo=tz)
        case "end":
            return datetime.combine(d, time.max, tzinfo=tz)
        case "noon":
            return datetime.combine(d, time(12, 0, 0), tzinfo=tz)
        case _:
            raise ValueError(f"Unsupported date_boundary_policy: {policy}")
