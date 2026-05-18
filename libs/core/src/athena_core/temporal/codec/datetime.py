from datetime import date, datetime, time
from email.utils import format_datetime as format_rfc5322_datetime
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo

from athena_core.temporal.codec.options import (
    DateBoundaryPolicy,
    DatetimeCodecOptions,
    DateTimeDecodeTarget,
    NaiveDateTimePolicy,
    TimestampUnit,
)
from athena_core.temporal.timezone import (
    coerce_timezone,
    get_timezone,
    is_aware_datetime,
    normalize_datetime_timezone,
)
from athena_core.values.fallbacks import first_non_empty

type DateTimeInput = str | int | float | datetime | date
type DateTimeOutput = datetime | int | str


class DateTimeCodec:
    """用于在外部日期时间值和 `datetime.datetime` 之间进行转换的编解码器

    该类将 `datetime.datetime` 作为归一化后的内部表示：
        - `encode()` 负责将外部值转换为 `datetime.datetime`。
        - `decode()` 负责将 `datetime.datetime` 转换为字符串、时间戳、ISO 字符串、RFC 5322 字符串，或者保持为 `datetime.datetime`。
    """

    def __init__(self, options: DatetimeCodecOptions | None = None):
        self._options = options or DatetimeCodecOptions()

    def encode(
        self,
        value: DateTimeInput,
        timezone: str | ZoneInfo | None = None,
        *,
        formats: list[str] | tuple[str, ...] | None = None,
        timestamp_unit: TimestampUnit | None = None,
        naive_policy: NaiveDateTimePolicy | None = None,
        date_boundary_policy: DateBoundaryPolicy | None = None,
    ) -> datetime:
        """将外部日期时间值转换为带时区的 `datetime`

        - 支持的输入包括 `datetime`、`date`、Unix 时间戳和日期时间字符串。
        - 无时区的 `datetime` 会根据 `naive_policy` 处理。
        - 纯 `date` 会根据 `date_boundary_policy` 转换到一天中的某个时间点。
        """
        tz = coerce_timezone(timezone or get_timezone())  # Always has a timezone
        match value:
            case datetime():
                return self._from_datetime(value, tz, naive_policy=naive_policy)
            case date():
                return self._from_date(value, tz, date_boundary_policy=date_boundary_policy)
            case int() | float():
                return self._from_timestamp(value, tz, unit=timestamp_unit)
            case str():
                return self._parse(value.strip(), tz, formats=formats)
            case _:
                raise ValueError(f"Unsupported value type: {type(value).__name__}.")

    def decode(
        self,
        value: datetime,
        timezone: str | ZoneInfo | None = None,
        *,
        target: DateTimeDecodeTarget | None = None,
        format: str | None = None,
    ) -> DateTimeOutput:
        """将 `datetime` 转换为配置指定的外部表示

        输入的 `datetime` 会先被归一化到目标时区，然后根据 `target` 转换格式。
        """
        tz = coerce_timezone(timezone or get_timezone())  # Always has a timezone
        dt = normalize_datetime_timezone(value, tz=tz)

        resolved_target = target or self._options.decode_target
        match resolved_target:
            case "datetime":
                return dt
            case "timestamp_ms":
                return int(dt.timestamp() * 1000)
            case "timestamp_s":
                return int(dt.timestamp())
            case "string":
                return dt.strftime(format or self._options.datetime_string_format)
            case "iso":
                return dt.isoformat()
            case "rfc5322":
                return format_rfc5322_datetime(dt)
            case _:
                raise ValueError(f"Unsupported datetime decode target: {resolved_target}.")

    def _from_datetime(
        self,
        dt: datetime,
        tz: ZoneInfo,
        *,
        naive_policy: NaiveDateTimePolicy | None,
    ) -> datetime:
        if not is_aware_datetime(dt) and (naive_policy or self._options.naive_policy) == "raise":
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

    def _from_timestamp(self, timestamp: int | float, tz: ZoneInfo, *, unit: TimestampUnit | None):
        unit = unit or self._options.timestamp_unit

        if unit == "ms":
            return datetime.fromtimestamp(timestamp / 1000, tz=tz)
        if unit == "s":
            return datetime.fromtimestamp(timestamp, tz=tz)
        raise ValueError(f"Unsupported timestamp unit: {unit}")

    def _parse(self, dt_str: str, tz: ZoneInfo, *, formats: list[str] | None):
        for format in first_non_empty(formats, list(self._options.datetime_formats)):
            try:
                if format == "iso":
                    dt = datetime.fromisoformat(dt_str)
                elif format == "rfc5322":
                    dt = parsedate_to_datetime(dt_str)
                else:
                    dt = datetime.strptime(dt_str, format)
                return normalize_datetime_timezone(dt, tz=tz)
            except (TypeError, ValueError):
                continue
        raise ValueError(f"Unsupported datetime string format: {dt_str}")


def parse_datetime(
    value: DateTimeInput,
    timezone: str | ZoneInfo | None = None,
    *,
    options: DatetimeCodecOptions | None = None,
    formats: list[str] | tuple[str, ...] | None = None,
    timestamp_unit: TimestampUnit | None = None,
    naive_policy: NaiveDateTimePolicy | None = None,
    date_boundary_policy: DateBoundaryPolicy | None = None,
) -> datetime:
    """将输入值解析或归一化为带时区的 `datetime`

    这是 `DateTimeCodec.encode()` 的函数式快捷入口。
    """
    return DateTimeCodec(options).encode(
        value,
        timezone=timezone,
        formats=formats,
        timestamp_unit=timestamp_unit,
        naive_policy=naive_policy,
        date_boundary_policy=date_boundary_policy,
    )


def format_datetime(
    value: datetime,
    timezone: str | ZoneInfo | None = None,
    *,
    options: DatetimeCodecOptions | None = None,
    target: DateTimeDecodeTarget | None = None,
    format: str | None = None,
) -> DateTimeOutput:
    """将 `datetime` 格式化为配置指定的外部表示

    这是 `DateTimeCodec.decode()` 的函数式快捷入口。
    """
    return DateTimeCodec(options).decode(
        value,
        timezone=timezone,
        target=target,
        format=format,
    )
