from datetime import datetime, time
from zoneinfo import ZoneInfo

from athena_core.temporal.base import TimeOutputFormat
from athena_core.temporal.codec.options import TimeCodecOptions
from athena_core.temporal.normalize import normalize_datetime_timezone
from athena_core.temporal.timezone import coerce_timezone, get_timezone
from athena_core.values.fallbacks import first_non_empty

type TimeInput = str | datetime | time
type TimeOutput = time | str


class TimeCodec:
    """用于在外部时间值和 `datetime.time` 之间转换的编解码器"""

    def __init__(self, options: TimeCodecOptions | None = None) -> None:
        self._options = options or TimeCodecOptions()

    def encode(
        self,
        value: TimeInput,
        timezone: str | ZoneInfo | None = None,
        *,
        parse_patterns: list[str] | tuple[str, ...] | None = None,
    ) -> time:
        tz = coerce_timezone(timezone or get_timezone())  # Always has a timezone
        match value:
            case datetime():
                return normalize_datetime_timezone(value, tz=tz).time()
            case time():
                return value
            case str():
                return self._parse(value.strip(), patterns=parse_patterns)
            case _:
                raise ValueError(f"Unsupported time value type: {type(value).__name__}.")

    def decode(
        self,
        value: time,
        *,
        output_format: TimeOutputFormat | None = None,
        format_pattern: str | None = None,
    ) -> TimeOutput:
        resolved = output_format or self._options.output_format
        match resolved:
            case "native":
                return value
            case "formatted":
                return value.strftime(format_pattern or self._options.format_pattern)
            case "iso":
                return value.isoformat()
            case _:
                raise ValueError(f"Unsupported time decode target: {resolved}.")

    def _parse(self, t_str: str, *, patterns: list[str] | tuple[str, ...] | None) -> time:
        if not t_str:
            raise ValueError("Time string cannot be empty.")

        candidate_patterns = first_non_empty(patterns, self._options.parse_patterns)
        for fmt in candidate_patterns:
            try:
                if fmt == "iso":
                    return time.fromisoformat(t_str)
                return datetime.strptime(t_str, fmt).time()
            except ValueError:
                continue
        raise ValueError(f"Unsupported time string format: {t_str}.")


def parse_time(
    value: TimeInput,
    timezone: str | ZoneInfo | None = None,
    *,
    options: TimeCodecOptions | None = None,
    parse_patterns: list[str] | tuple[str, ...] | None = None,
) -> time:
    """将输入值解析或归一化为 `time`"""
    return TimeCodec(options).encode(
        value,
        timezone,
        parse_patterns=parse_patterns,
    )


def format_time(
    value: time,
    *,
    options: TimeCodecOptions | None = None,
    output_format: TimeOutputFormat | None = None,
    format_pattern: str | None = None,
) -> TimeOutput:
    """将 `time` 格式化为配置指定的外部表示"""
    return TimeCodec(options).decode(
        value,
        output_format=output_format,
        format_pattern=format_pattern,
    )
