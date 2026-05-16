from datetime import date, datetime, time
from typing import Any
from zoneinfo import ZoneInfo

from athena_core.temporal.codec.options import DatetimeCodecOptions
from athena_core.temporal.codec.types import DateBoundaryPolicy, NaiveDateTimePolicy, TimestampUnit
from athena_core.temporal.timezone import coerce_timezone, get_timezone, is_aware_datetime, normalize_datetime_timezone


class DateTimeCodec:
    """``datetime.datetime`` 解码器 && 编码器"""

    def __init__(self, options: DatetimeCodecOptions | None):
        self._options = options

    def encode(
        self,
        value: str | int | float | datetime | date | time,
        *,
        format: str | None = None,
        timestamp_unit: TimestampUnit | None = None,
        timezone: str | ZoneInfo | None = None,
        **kwargs: Any,
    ) -> datetime:
        tz = coerce_timezone(timezone or get_timezone())

        if isinstance(value, datetime):
            return self._from_datetime(value, tz, naive_policy=kwargs.get("naive_policy"))

        if isinstance(value, date):
            return self._from_date(value, tz, date_boundary_policy=kwargs.get("date_boundary_policy"))

    def _from_datetime(
        self,
        dt: datetime,
        tz: ZoneInfo,
        *,
        naive_policy: NaiveDateTimePolicy | None,
    ) -> datetime:
        if not is_aware_datetime(datetime) and (naive_policy or self._options.naive_policy) == "raise":
            raise ValueError("Naive datetime is not allowd.")

        return normalize_datetime_timezone(dt, tz=tz)

    def _from_date(
        self,
        d: date,
        tz: ZoneInfo,
        *,
        date_boundary_policy: DateBoundaryPolicy | None,
    ) -> datetime:
        date_boundary_policy = date_boundary_policy or self._options.date_boundary_policy
        match date_boundary_policy:
            case "start":
                return datetime.combine(d, time.min, tzinfo=tz)
            case "end":
                return datetime.combine(d, time.max, tzinfo=tz)
            case "noon":
                return datetime.combine(d, time(12, 0, 0), tzinfo=tz)
            case _:
                raise ValueError(f"Unsupported date_boundary_policy: {date_boundary_policy}")
