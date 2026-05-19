from datetime import date, datetime
from email.utils import format_datetime as format_rfc5322_datetime
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo

from athena_core.temporal.codec.options import DateTimeCodecOptions
from athena_core.temporal.normalize import normalize_datetime_timezone, resolve_date_boundary
from athena_core.temporal.predicates import is_naive_datetime
from athena_core.temporal.timezone import coerce_timezone, get_timezone
from athena_core.temporal.types import (
    DateBoundaryPolicy,
    DateTimeOutputFormat,
    NaiveDateTimePolicy,
    TimestampUnit,
)
from athena_core.values.fallbacks import first_non_empty

type DateTimeInput = str | int | float | datetime | date
type DateTimeOutput = datetime | int | str


class DateTimeCodec:
    """用于在外部日期时间值和 `datetime.datetime` 之间进行转换的编解码器"""

    def __init__(self, options: DateTimeCodecOptions | None = None):
        self._options = options or DateTimeCodecOptions()

    def parse(
        self,
        value: DateTimeInput,
        timezone: str | ZoneInfo | None = None,
        *,
        parse_patterns: list[str] | tuple[str, ...] | None = None,
        timestamp_unit: TimestampUnit | None = None,
        naive_datetime_policy: NaiveDateTimePolicy | None = None,
        boundary_policy: DateBoundaryPolicy | None = None,
    ) -> datetime:
        """将外部日期时间值转换为带时区的 `datetime`"""
        tz = coerce_timezone(timezone) if timezone is not None else get_timezone()
        match value:
            # `datetime` is a subclass of `date`, so this case must appear first.
            case datetime():
                return self._from_datetime(value, tz, naive_datetime_policy=naive_datetime_policy)
            case date():
                return resolve_date_boundary(value, tz, boundary_policy=boundary_policy or self._options.boundary_policy)
            case int() | float():
                return self._from_timestamp(value, tz, timestamp_unit=timestamp_unit)
            case str():
                return self._parse(value.strip(), tz, patterns=parse_patterns)
            case _:
                raise ValueError(f"Unsupported value type: {type(value).__name__}.")

    def format(
        self,
        value: datetime,
        timezone: str | ZoneInfo | None = None,
        *,
        output_format: DateTimeOutputFormat | None = None,
        format_pattern: str | None = None,
    ) -> DateTimeOutput:
        """将 `datetime` 转换为配置指定的外部表示"""
        tz = coerce_timezone(timezone) if timezone is not None else get_timezone()  # Always has a timezone
        dt = normalize_datetime_timezone(value, tz=tz)

        resolved = output_format or self._options.output_format
        match resolved:
            case "native":
                return dt
            case "iso":
                return dt.isoformat()
            case "rfc5322":
                return format_rfc5322_datetime(dt)
            case "formatted":
                return dt.strftime(format_pattern or self._options.format_pattern)
            case "timestamp_ms":
                return int(dt.timestamp() * 1000)
            case "timestamp_s":
                return int(dt.timestamp())
            case _:
                raise ValueError(f"Unsupported datetime output format: {resolved}.")

    def _from_datetime(
        self,
        dt: datetime,
        tz: ZoneInfo,
        *,
        naive_datetime_policy: NaiveDateTimePolicy | None,
    ) -> datetime:
        if is_naive_datetime(dt) and (naive_datetime_policy or self._options.naive_datetime_policy) == "raise":
            raise ValueError("Naive datetime is not allowed.")
        return normalize_datetime_timezone(dt, tz=tz)

    def _from_timestamp(self, timestamp: int | float, tz: ZoneInfo, *, timestamp_unit: TimestampUnit | None):
        resolved = timestamp_unit or self._options.timestamp_unit
        if resolved == "ms":
            return datetime.fromtimestamp(timestamp / 1000, tz=tz)
        if resolved == "s":
            return datetime.fromtimestamp(timestamp, tz=tz)
        raise ValueError(f"Unsupported timestamp unit: {resolved}")

    def _parse(self, dt_str: str, tz: ZoneInfo, *, patterns: list[str] | tuple[str, ...] | None):
        if not dt_str:
            raise ValueError("DateTime string cannot be empty.")

        candidate_patterns = first_non_empty(patterns, self._options.parse_patterns)
        for fmt in candidate_patterns:
            try:
                if fmt == "iso":
                    dt = datetime.fromisoformat(dt_str)
                elif fmt == "rfc5322":
                    dt = parsedate_to_datetime(dt_str)
                else:
                    dt = datetime.strptime(dt_str, fmt)
                return normalize_datetime_timezone(dt, tz=tz)
            except ValueError:
                continue
        raise ValueError(f"Unsupported datetime string format: {dt_str}")


def parse_datetime(
    value: DateTimeInput,
    timezone: str | ZoneInfo | None = None,
    *,
    options: DateTimeCodecOptions | None = None,
    parse_patterns: list[str] | tuple[str, ...] | None = None,
    timestamp_unit: TimestampUnit | None = None,
    naive_datetime_policy: NaiveDateTimePolicy | None = None,
    boundary_policy: DateBoundaryPolicy | None = None,
) -> datetime:
    """将输入值解析或归一化为带时区的 `datetime`"""
    return DateTimeCodec(options).parse(
        value,
        timezone,
        parse_patterns=parse_patterns,
        timestamp_unit=timestamp_unit,
        naive_datetime_policy=naive_datetime_policy,
        boundary_policy=boundary_policy,
    )


def format_datetime(
    value: datetime,
    timezone: str | ZoneInfo | None = None,
    *,
    options: DateTimeCodecOptions | None = None,
    output_format: DateTimeOutputFormat | None = None,
    format_pattern: str | None = None,
) -> DateTimeOutput:
    """将 `datetime` 格式化为配置指定的外部表示"""
    return DateTimeCodec(options).format(
        value,
        timezone,
        output_format=output_format,
        format_pattern=format_pattern,
    )
