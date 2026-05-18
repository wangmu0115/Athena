from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

type TimestampUnit = Literal["s", "ms"]
type NaiveDateTimePolicy = Literal["assume_local", "raise"]
type DateBoundaryPolicy = Literal["start", "end", "noon"]
type DateTimeDecodeTarget = Literal[
    "datetime",
    "timestamp_s",
    "timestamp_ms",
    "string",
    "iso",
    "rfc5322",
]


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
