from pydantic import BaseModel, ConfigDict, Field

from athena_kit.core.temporal.types import (
    DateBoundaryPolicy,
    DateOutputFormat,
    DateTimeOutputFormat,
    NaiveDateTimePolicy,
    TimeOutputFormat,
    TimestampUnit,
)

DEFAULT_DATE_FORMATS: tuple[str, ...] = (
    "iso",
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y%m%d",
)

DEFAULT_TIME_FORMATS: tuple[str, ...] = (
    "iso",
    "%H:%M:%S",
    "%H:%M",
    "%H%M%S",
    "%H%M",
)

DEFAULT_DATETIME_FORMATS: tuple[str, ...] = (
    "iso",
    "rfc5322",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d %H:%M",
    "%Y%m%d %H%M%S",
    "%Y%m%d %H%M",
    "%Y%m%d_%H%M%S",
    "%Y%m%d_%H%M",
)


class _BaseCodecOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",                  # 禁止未知字段
        arbitrary_types_allowed=True,    # 允许自定义对象
        validate_assignment=True,        # 修改字段重新校验
        str_strip_whitespace=True,       # 自动 trim
    )  # fmt: off


class DateCodecOptions(_BaseCodecOptions):
    parse_patterns: tuple[str, ...] = Field(
        DEFAULT_DATE_FORMATS,
        min_length=1,
        description="用于解析日期字符串的 `strptime` 格式列表",
    )
    output_format: DateOutputFormat = Field("formatted", description="日期输出格式")
    format_pattern: str = Field("%Y-%m-%d", description="当 `output_format` 为 `formatted` 时使用的 `strftime` 格式")

    boundary_policy: DateBoundaryPolicy = Field("start", description="`date` 补全为 `datetime` 时使用的时间边界策略")
    timestamp_unit: TimestampUnit = Field("s", description="时间戳单位")


class TimeCodecOptions(_BaseCodecOptions):
    parse_patterns: tuple[str, ...] = Field(
        DEFAULT_TIME_FORMATS,
        min_length=1,
        description="用于解析时间字符串的 `strptime` 格式列表",
    )
    output_format: TimeOutputFormat = Field("formatted", description="时间输出格式")
    format_pattern: str = Field("%H:%M:%S", description="当 `output_format` 为 `formatted` 时使用的 `strftime` 格式")


class DateTimeCodecOptions(_BaseCodecOptions):
    parse_patterns: tuple[str, ...] = Field(
        DEFAULT_DATETIME_FORMATS,
        min_length=1,
        description="用于解析日期时间字符串的 `strptime` 格式列表",
    )
    output_format: DateTimeOutputFormat = Field("formatted", description="日期时间输出格式")
    format_pattern: str = Field(
        "%Y-%m-%d %H:%M:%S", description="当 `output_format` 为 `formatted` 时使用的 `strftime` 格式"
    )

    naive_datetime_policy: NaiveDateTimePolicy = Field(
        "assume_timezone",
        description="naive datetime 处理策略，该选项不适用于按已配置模式解析的字符串输入",
    )
    boundary_policy: DateBoundaryPolicy = Field("start", description="`date` 补全为 `datetime` 时使用的时间边界策略")
    timestamp_unit: TimestampUnit = Field("s", description="时间戳单位")


class TemporalCodecOptions(_BaseCodecOptions):
    time: TimeCodecOptions = Field(default_factory=TimeCodecOptions, description="时间编解码器配置项")
    date: DateCodecOptions = Field(default_factory=DateCodecOptions, description="日期编解码器配置项")
    datetime: DateTimeCodecOptions = Field(default_factory=DateTimeCodecOptions, description="日期时间编解码器配置项")
