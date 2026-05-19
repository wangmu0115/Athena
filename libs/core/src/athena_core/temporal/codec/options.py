from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from athena_core.temporal.base import TimeOutputFormat

type TimestampUnit = Literal["s", "ms"]
type NaiveDateTimePolicy = Literal["assume_local", "raise"]
type DateBoundaryPolicy = Literal["start", "end", "noon"]

type TimeDecodeTarget = Literal["time", "string", "iso"]
type DateDecodeTarget = Literal["date", "datetime", "string", "iso", "timestamp_s", "timestamp_ms"]
type DateTimeDecodeTarget = Literal["datetime", "timestamp_s", "timestamp_ms", "string", "iso", "rfc5322"]

type TemporalDecodeTarget = DateDecodeTarget | TimeDecodeTarget | DateTimeDecodeTarget

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
    "%Y-%m-%d",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d %H:%M",
    "%Y/%m/%d",
    "%Y%m%d %H%M%S",
    "%Y%m%d %H%M",
    "%Y%m%d",
    "%Y%m%d_%H%M%S",
    "%Y%m%d_%H%M",
    "%Y%m%d",
)


class BaseOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",                  # 禁止未知字段
        arbitrary_types_allowed=True,    # 允许自定义对象
        validate_assignment=True,        # 修改字段重新校验
        str_strip_whitespace=True,       # 自动 trim
    )  # fmt: off


class DateCodecOptions(BaseOptions):
    """Options for `DateCodec`.

    `DateCodec` 的配置。
    """

    date_formats: tuple[str, ...] = Field(
        DEFAULT_DATE_FORMATS,
        min_length=1,
        description="日期字符串解析格式",
    )
    decode_target: DateDecodeTarget = Field("string", description="date 解码目标")
    date_string_format: str = Field("%Y-%m-%d", description="解码为 string 时的日期格式")
    date_boundary_policy: DateBoundaryPolicy = Field(
        "start",
        description="date 转换为 datetime 时映射到一天中的时间点",
    )
    timestamp_unit: TimestampUnit = Field("ms", description="时间戳单位")


class TimeCodecOptions(BaseOptions):
    parse_patterns: tuple[str, ...] = Field(
        DEFAULT_TIME_FORMATS,
        min_length=1,
        description="用于解析时间字符串的 `strptime` 格式列表",
    )
    output_format: TimeOutputFormat = Field("formatted", description="时间输出格式")
    format_pattern: str = Field(
        "%H:%M:%S",
        description="当 `output_format` 为 `formatted` 时使用的 `strftime` 格式",
    )


class DatetimeCodecOptions(BaseOptions):
    naive_policy: NaiveDateTimePolicy = Field("assume_local", description="无时区 datetime 处理方式")
    date_boundary_policy: DateBoundaryPolicy = Field("start", description="date 转换为 datetime 时，映射到一天的时间点")
    timestamp_unit: TimestampUnit = Field("ms", description="时间戳单位")
    datetime_formats: tuple[str, ...] = Field(
        DEFAULT_DATETIME_FORMATS,
        min_length=1,
        description="日期时间字符串转换为 datetime 的格式",
    )

    decode_target: DateTimeDecodeTarget = Field("string", description="datetime 解码目标")
    datetime_string_format: str = Field("%Y-%m-%d %H:%M:%S", description="解码为 string 时的格式")


class TemporalCodecOptions(BaseOptions):
    """Options for `TemporalCodec`.

    `TemporalCodec` 的组合配置。
    """

    date: DateCodecOptions = Field(default_factory=DateCodecOptions)
    time: TimeCodecOptions = Field(default_factory=TimeCodecOptions)
    datetime: DatetimeCodecOptions = Field(default_factory=DatetimeCodecOptions)
