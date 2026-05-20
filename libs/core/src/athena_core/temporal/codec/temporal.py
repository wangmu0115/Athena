from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from athena_core.temporal.codec.date import DateCodec, DateInput, DateOutput
from athena_core.temporal.codec.datetime import DateTimeCodec, DateTimeInput, DateTimeOutput
from athena_core.temporal.codec.options import TemporalCodecOptions
from athena_core.temporal.codec.time import TimeCodec, TimeInput, TimeOutput
from athena_core.temporal.types import (
    DateBoundaryPolicy,
    DateOutputFormat,
    DateTimeOutputFormat,
    NaiveDateTimePolicy,
    TimeOutputFormat,
    TimestampUnit,
)


class TemporalCodec:
    """门面入口解码器&编码器，包括：时间解码器&编码器、日期解码器&编码器和日期时间解码器&编码器。"""

    def __init__(self, options: TemporalCodecOptions | None = None):
        self._options = options or TemporalCodecOptions()
        self._time_codec = TimeCodec(self._options.time)
        self._date_codec = DateCodec(self._options.date)
        self._datetime_codec = DateTimeCodec(self._options.datetime)

    def parse_time(
        self,
        value: TimeInput,
        timezone: str | ZoneInfo | None = None,
        *,
        parse_patterns: list[str] | tuple[str, ...] | None = None,
    ) -> time:
        """将输入值解析 `time`。

        详见：`TimeCodec.parse()`
        """
        return self._time_codec.parse(
            value,
            timezone,
            parse_patterns=parse_patterns,
        )

    def format_time(
        self,
        value: time,
        *,
        output_format: TimeOutputFormat | None = None,
        format_pattern: str | None = None,
    ) -> TimeOutput:
        """将 `time` 格式化为指定外部表示。

        详见：`TimeCodec.format()`
        """
        return self._time_codec.format(
            value,
            output_format=output_format,
            format_pattern=format_pattern,
        )

    def parse_date(
        self,
        value: DateInput,
        timezone: str | ZoneInfo | None = None,
        *,
        parse_patterns: list[str] | tuple[str, ...] | None = None,
        timestamp_unit: TimestampUnit | None = None,
    ) -> date:
        """将输入值解析为 `date`。

        详见：`DateCodec.parse()`
        """
        return self._date_codec.parse(
            value,
            timezone,
            parse_patterns=parse_patterns,
            timestamp_unit=timestamp_unit,
        )

    def format_date(
        self,
        value: date,
        timezone: str | ZoneInfo | None = None,
        *,
        output_format: DateOutputFormat | None = None,
        format_pattern: str | None = None,
        boundary_policy: DateBoundaryPolicy | None = None,
    ) -> DateOutput:
        """将 `date` 格式化为指定外部表示，格式化为 `datetime` 或时间戳时会归一化到目标时区。

        详见：`DateCodec.format()`
        """
        return self._date_codec.format(
            value,
            timezone,
            output_format=output_format,
            format_pattern=format_pattern,
            boundary_policy=boundary_policy,
        )

    def parse_datetime(
        self,
        value: DateTimeInput,
        timezone: str | ZoneInfo | None = None,
        *,
        parse_patterns: list[str] | tuple[str, ...] | None = None,
        timestamp_unit: TimestampUnit | None = None,
        naive_datetime_policy: NaiveDateTimePolicy | None = None,
        boundary_policy: DateBoundaryPolicy | None = None,
    ) -> datetime:
        """将输入值解析或归一化为带时区信息的 `datetime`。

        详见：`DateTimeCodec.parse()`
        """
        return self._datetime_codec.parse(
            value,
            timezone,
            parse_patterns=parse_patterns,
            timestamp_unit=timestamp_unit,
            naive_datetime_policy=naive_datetime_policy,
            boundary_policy=boundary_policy,
        )

    def format_datetime(
        self,
        value: datetime,
        timezone: str | ZoneInfo | None = None,
        *,
        output_format: DateTimeOutputFormat | None = None,
        format_pattern: str | None = None,
    ) -> DateTimeOutput:
        """将 `datetime` 格式化为指定外部表示，格式化前会先将输入时间归一化到目标时区。

        详见：`DateTimeCodec.format()`
        """
        return self._datetime_codec.format(
            value,
            timezone,
            output_format=output_format,
            format_pattern=format_pattern,
        )
