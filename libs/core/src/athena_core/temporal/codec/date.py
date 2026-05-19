from datetime import date, datetime
from zoneinfo import ZoneInfo

from athena_core.temporal.codec.options import DateCodecOptions
from athena_core.temporal.normalize import normalize_datetime_timezone, resolve_date_boundary
from athena_core.temporal.timezone import coerce_timezone, get_timezone
from athena_core.temporal.types import DateBoundaryPolicy, DateOutputFormat, TimestampUnit
from athena_core.values.fallbacks import first_non_empty

type DateInput = str | int | float | datetime | date
type DateOutput = date | datetime | int | str


class DateCodec:
    """用于在外部日期值和 `datetime.date` 之间转换的编解码器"""

    def __init__(self, options: DateCodecOptions | None = None):
        self._options = options or DateCodecOptions()

    def parse(
        self,
        value: DateInput,
        timezone: str | ZoneInfo | None = None,
        *,
        parse_patterns: list[str] | tuple[str, ...] | None = None,
        timestamp_unit: TimestampUnit | None = None,
    ) -> date:
        tz = coerce_timezone(timezone) if timezone is not None else get_timezone()
        match value:
            case datetime():
                return normalize_datetime_timezone(value, tz=tz).date()
            case date():
                return value
            case int() | float():
                return self._from_timestamp(value, tz, timestamp_unit=timestamp_unit)
            case str():
                return self._parse(value.strip(), patterns=parse_patterns)
            case _:
                raise ValueError(f"Unsupported date value type: {type(value).__name__}.")

    def format(
        self,
        value: date,
        timezone: str | ZoneInfo | None = None,
        *,
        output_format: DateOutputFormat | None = None,
        format_pattern: str | None = None,
        boundary_policy: DateBoundaryPolicy | None = None,
    ) -> DateOutput:
        tz = coerce_timezone(timezone) if timezone is not None else get_timezone()

        resolved = output_format or self._options.output_format
        match resolved:
            case "native":
                return value
            case "iso":
                return value.isoformat()
            case "formatted":
                return value.strftime(format_pattern or self._options.format_pattern)
            case "datetime":
                return resolve_date_boundary(value, tz, boundary_policy=boundary_policy or self._options.boundary_policy)
            case "timestamp_s" | "timestamp_ms":
                dt = resolve_date_boundary(value, tz, boundary_policy=boundary_policy or self._options.boundary_policy)
                return int(dt.timestamp()) if resolved == "timestamp_s" else int(dt.timestamp() * 1000)
            case _:
                raise ValueError(f"Unsupported date output format: {resolved}.")

    def _from_timestamp(
        self,
        timestamp: int | float,
        tz: ZoneInfo,
        *,
        timestamp_unit: TimestampUnit | None,
    ) -> date:
        resolved = timestamp_unit or self._options.timestamp_unit
        if resolved == "ms":
            return datetime.fromtimestamp(timestamp / 1000, tz=tz).date()
        if resolved == "s":
            return datetime.fromtimestamp(timestamp, tz=tz).date()
        raise ValueError(f"Unsupported timestamp unit: {resolved}.")

    def _parse(self, d_str: str, *, patterns: list[str] | tuple[str, ...] | None) -> date:
        if not d_str:
            raise ValueError("Date string cannot be empty.")

        candidate_patterns = first_non_empty(patterns, self._options.parse_patterns)
        for fmt in candidate_patterns:
            try:
                if fmt == "iso":
                    return date.fromisoformat(d_str)
                return datetime.strptime(d_str, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Unsupported date string format: {d_str}.")


def parse_date(
    value: DateInput,
    timezone: str | ZoneInfo | None = None,
    *,
    options: DateCodecOptions | None = None,
    parse_patterns: list[str] | tuple[str, ...] | None = None,
    timestamp_unit: TimestampUnit | None = None,
) -> date:
    """将输入值解析或归一化为 `date`"""
    return DateCodec(options).parse(
        value,
        timezone,
        parse_patterns=parse_patterns,
        timestamp_unit=timestamp_unit,
    )


def format_date(
    value: date,
    timezone: str | ZoneInfo | None = None,
    *,
    options: DateCodecOptions | None = None,
    output_format: DateOutputFormat | None = None,
    format_pattern: str | None = None,
    boundary_policy: DateBoundaryPolicy | None = None,
) -> DateOutput:
    """将 `date` 格式化为配置指定的外部表示"""
    return DateCodec(options).format(
        value,
        timezone,
        output_format=output_format,
        format_pattern=format_pattern,
        boundary_policy=boundary_policy,
    )
