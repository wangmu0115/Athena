from datetime import datetime, time
from zoneinfo import ZoneInfo

from athena_kit.core.temporal.codec.options import TimeCodecOptions
from athena_kit.core.temporal.normalize import normalize_datetime_timezone
from athena_kit.core.temporal.timezone import coerce_timezone, get_timezone
from athena_kit.core.temporal.types import TimeOutputFormat
from athena_kit.core.values.fallbacks import first_non_empty
from athena_kit.core.values.optional import optional_or_else

type TimeInput = str | datetime | time
type TimeOutput = time | str


class TimeCodec:
    """时间解码器&编码器，该类负责在外部时间表示和 Python `datetime.time` 之间转换。

    支持的输入包括：
    - `time`：原样返回。
    - `datetime`：先转换到目标时区，再取时间部分。
    - `str`：按照 `parse_patterns` 解析为时间。

    注意：
        从 `datetime` 提取时间时会丢弃日期和时区信息，返回的是目标时区下的墙上时间。
    """

    def __init__(self, options: TimeCodecOptions | None = None) -> None:
        self._options = options or TimeCodecOptions()

    def parse(
        self,
        value: TimeInput,
        timezone: str | ZoneInfo | None = None,
        *,
        parse_patterns: list[str] | tuple[str, ...] | None = None,
    ) -> time:
        """将输入值解析 `time`。

        Args:
            value: 时间输入值。
            timezone: 目标时区，未传入时使用当前有效时区，用于当输入时 `datetime` 时，先归一化到目标时区。
            parse_patterns: 字符串解析格式列表，未传入时使用配置中的默认格式。

        Returns:
            目标时区下的墙上时间。

        Raises:
            ValueError: 当输入类型不受支持或字符串格式无法解析时抛出。
        """
        tz = coerce_timezone(optional_or_else(timezone, default_factory=get_timezone))
        match value:
            case datetime():
                return normalize_datetime_timezone(value, tz=tz).time()
            case time():
                return value
            case str():
                return self._parse(value.strip(), patterns=parse_patterns)
            case _:
                raise ValueError(f"Unsupported time output format: {type(value).__name__}.")

    def format(
        self,
        value: time,
        *,
        output_format: TimeOutputFormat | None = None,
        format_pattern: str | None = None,
    ) -> TimeOutput:
        """将 `time` 格式化为指定外部表示。

        Args:
            value: 需要格式化的 `datetime`。
            output_format: 输出表示格式，未传入时使用配置中的默认格式。
            format_pattern: 当 `output_format` 为 `formatted` 时使用的 `strftime` 格式。

        Returns:
            根据 `output_format` 返回 `time` 或时间戳。

        Raises:
            ValueError: 当输出表示格式不受支持时抛出。
        """
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
    """将输入值解析 `time`。

    此函数是 `TimeCodec.parse()` 的函数式快捷入口。
    """
    return TimeCodec(options).parse(
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
    """将 `time` 格式化为指定外部表示。

    此函数是 `TimeCodec.format()` 的函数式快捷入口。
    """
    return TimeCodec(options).format(
        value,
        output_format=output_format,
        format_pattern=format_pattern,
    )
