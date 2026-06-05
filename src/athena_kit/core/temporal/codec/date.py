from datetime import date, datetime
from zoneinfo import ZoneInfo

from athena_kit.core.temporal.codec.options import DateCodecOptions
from athena_kit.core.temporal.normalize import normalize_datetime_timezone, resolve_date_boundary
from athena_kit.core.temporal.timezone import coerce_timezone, get_timezone
from athena_kit.core.temporal.types import DateBoundaryPolicy, DateOutputFormat, TimestampUnit
from athena_kit.core.values.fallbacks import first_non_empty
from athena_kit.core.values.optional import optional_or_else

type DateInput = str | int | float | datetime | date
type DateOutput = date | datetime | int | str


class DateCodec:
    """日期解码器&编码器，该类负责在外部日期表示和 Python `datetime.date` 之间转换。

    支持的输入包括：
    - `date`：原样返回。
    - `datetime`：先转换到目标时区，再取日期部分。
    - `int` / `float`：按照 `timestamp_unit` 解释为 Unix 时间戳。
    - `str`：按照 `parse_patterns` 解析为日期。

    注意：
        字符串输入只按日期格式解析，不默认解析日期时间字符串。
    """

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
        """将输入值解析为 `date`。

        Args:
            value: 日期输入值。
            timezone: 目标时区，未传入时使用当前有效时区，用于将 `datetime` 和时间戳先归一化到目标时区的日期时间类型。
            parse_patterns: 字符串解析格式列表，未传入时使用配置中的默认格式。
            timestamp_unit: 数字时间戳单位，未传入时使用配置中的默认单位。

        Returns:
            `date`

        Raises:
            ValueError: 当输入类型不受支持或字符串格式无法解析时抛出。
        """
        tz = coerce_timezone(optional_or_else(timezone, default_factory=get_timezone))
        match value:
            # `datetime` is a subclass of `date`, so this case must appear first.
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
        """将 `date` 格式化为指定外部表示，格式化为 `datetime` 或时间戳时会归一化到目标时区。

        Args:
            value: 需要格式化的 `date`。
            timezone: 目标时区，未传入时使用当前有效时区，用于输出表示为 `datetime` 或时间戳。
            output_format: 输出表示格式，未传入时使用配置中的默认格式。
            format_pattern: 当 `output_format` 为 `formatted` 时使用的 `strftime` 格式。
            boundary_policy: `date` 补全为 `datetime` 时使用的边界策略。

        Returns:
            根据 `output_format` 返回 `date`、`datetime`、字符串或时间戳。

        Raises:
            ValueError: 当输出表示格式不受支持时抛出。
        """
        tz = coerce_timezone(optional_or_else(timezone, default_factory=get_timezone))

        resolved = output_format or self._options.output_format
        match resolved:
            case "native":
                return value
            case "iso":
                return value.isoformat()
            case "formatted":
                return value.strftime(format_pattern or self._options.format_pattern)
            case "datetime":
                return resolve_date_boundary(
                    value, tz, boundary_policy=boundary_policy or self._options.boundary_policy
                )
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
    """将输入值解析为 `date`。

    此函数是 `DateCodec.parse()` 的函数式快捷入口。
    """
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
    """将 `date` 格式化为指定外部表示，格式化为 `datetime` 或时间戳时会归一化到目标时区。

    此函数是 `DateCodec.format()` 的函数式快捷入口。
    """
    return DateCodec(options).format(
        value,
        timezone,
        output_format=output_format,
        format_pattern=format_pattern,
        boundary_policy=boundary_policy,
    )
