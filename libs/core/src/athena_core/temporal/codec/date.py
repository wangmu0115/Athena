from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from athena_core.temporal.codec.options import DateBoundaryPolicy, DateCodecOptions, DateDecodeTarget, TimestampUnit
from athena_core.temporal.timezone import coerce_timezone, get_timezone, normalize_datetime_timezone
from athena_core.values.fallbacks import first_non_empty

type DateInput = str | int | float | datetime | date
type DateOutput = date | datetime | int | str


class DateCodec:
    """用于在外部日期值和 `datetime.date` 之间转换的编解码器"""

    def __init__(self, options: DateCodecOptions | None = None):
        self._options = options or DateCodecOptions()

    def encode(
        self,
        value: DateInput,
        timezone: str | ZoneInfo | None = None,
        *,
        formats: list[str] | tuple[str, ...] | None = None,
        timestamp_unit: TimestampUnit | None = None,
    ) -> date:
        tz = coerce_timezone(timezone or get_timezone())
        match value:
            case datetime():
                return normalize_datetime_timezone(value, tz=tz).date()
            case date():
                return value
            case int() | float():
                return self._from_timestamp(value, tz, unit=timestamp_unit)
            case str():
                return self._parse(value.strip(), formats)
            case _:
                raise ValueError(f"Unsupported date value type: {type(value).__name__}.")

    def decode(
        self,
        value: date,
        timezone: str | ZoneInfo | None = None,
        *,
        target: DateDecodeTarget | None = None,
        format: str | None = None,
        date_boundary_policy: DateBoundaryPolicy | None = None,
        timestamp_unit: TimestampUnit | None = None,
    ) -> DateOutput:
        resolved_target = target or self._options.decode_target
        match resolved_target:
            case "date":
                return value
            case "datetime":
                return self._to_datetime(value, timezone, date_boundary_policy=date_boundary_policy)
            case "timestamp_s":
                dt = self._to_datetime(value, timezone, date_boundary_policy=date_boundary_policy)
                return int(dt.timestamp())
            case "timestamp_ms":
                dt = self._to_datetime(value, timezone, date_boundary_policy=date_boundary_policy)
                return int(dt.timestamp() * 1000)
            case "string":
                return value.strftime(format or self._options.date_string_format)
            case "iso":
                return value.isoformat()
            case _:
                raise ValueError(f"Unsupported date decode target: {resolved_target}.")

    def _from_timestamp(self, timestamp: int | float, tz: ZoneInfo, *, unit: TimestampUnit | None) -> date:
        resolved_unit = unit or self._options.timestamp_unit

        if resolved_unit == "ms":
            return datetime.fromtimestamp(timestamp / 1000, tz=tz).date()
        if resolved_unit == "s":
            return datetime.fromtimestamp(timestamp, tz=tz).date()

        raise ValueError(f"Unsupported timestamp unit: {resolved_unit}.")

    def _parse(self, d_str: str, *, formats: list[str] | tuple[str, ...] | None) -> date:
        if not d_str:
            raise ValueError("Date string cannot be empty.")

        candidate_formats = first_non_empty(formats, self._options.date_formats)
        for fmt in candidate_formats:
            try:
                if fmt == "iso":
                    return date.fromisoformat(d_str)
                return datetime.strptime(d_str, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Unsupported date string format: {d_str}.")

    def _to_datetime(
        self,
        value: date,
        timezone: str | ZoneInfo | None,
        *,
        date_boundary_policy: DateBoundaryPolicy | None,
    ) -> datetime:
        """Convert `date` into timezone-aware `datetime`.

        将 `date` 转换为带时区的 `datetime`。
        """
        tz = coerce_timezone(timezone or get_timezone())
        resolved_policy = date_boundary_policy or self._options.date_boundary_policy

        match resolved_policy:
            case "start":
                return datetime.combine(value, time.min, tzinfo=tz)
            case "end":
                return datetime.combine(value, time.max, tzinfo=tz)
            case "noon":
                return datetime.combine(value, time(12, 0, 0), tzinfo=tz)
            case _:
                raise ValueError(f"Unsupported date boundary policy: {resolved_policy}.")
