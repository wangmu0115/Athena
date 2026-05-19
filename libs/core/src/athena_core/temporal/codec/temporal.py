from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from athena_core.temporal.codec.date import DateCodec, DateInput, DateOutput
from athena_core.temporal.codec.datetime import DateTimeCodec, DateTimeInput, DateTimeOutput
from athena_core.temporal.codec.options import (
    DateBoundaryPolicy,
    DateDecodeTarget,
    DateTimeDecodeTarget,
    NaiveDateTimePolicy,
    TemporalCodecOptions,
    TimeDecodeTarget,
    TimestampUnit,
)
from athena_core.temporal.codec.time import TimeCodec, TimeInput, TimeOutput

type TemporalInput = DateTimeInput | DateInput | TimeInput
type TemporalValue = datetime | date | time
type TemporalOutput = DateTimeOutput | DateOutput | TimeOutput


class TemporalCodec:
    """Facade codec for `date`, `time`, and `datetime`.

    `date`、`time` 和 `datetime` 的统一门面编解码器。
    """

    def __init__(self, options: TemporalCodecOptions | None = None) -> None:
        """Initialize the temporal codec.

        初始化统一时间编解码器。
        """
        self._options = options or TemporalCodecOptions()
        self.date = DateCodec(self._options.date)
        self.time = TimeCodec(self._options.time)
        self.datetime = DateTimeCodec(self._options.datetime)

    def encode_datetime(
        self,
        value: DateTimeInput,
        timezone: str | ZoneInfo | None = None,
        *,
        formats: list[str] | tuple[str, ...] | None = None,
        timestamp_unit: TimestampUnit | None = None,
        naive_policy: NaiveDateTimePolicy | None = None,
        date_boundary_policy: DateBoundaryPolicy | None = None,
    ) -> datetime:
        """Encode a value into `datetime`.

        将值编码为 `datetime`。
        """
        return self.datetime.encode(
            value,
            timezone=timezone,
            formats=formats,
            timestamp_unit=timestamp_unit,
            naive_policy=naive_policy,
            date_boundary_policy=date_boundary_policy,
        )

    def encode_date(
        self,
        value: DateInput,
        timezone: str | ZoneInfo | None = None,
        *,
        formats: list[str] | tuple[str, ...] | None = None,
        timestamp_unit: TimestampUnit | None = None,
    ) -> date:
        """Encode a value into `date`.

        将值编码为 `date`。
        """
        return self.date.encode(
            value,
            timezone=timezone,
            formats=formats,
            timestamp_unit=timestamp_unit,
        )

    def encode_time(
        self,
        value: TimeInput,
        *,
        formats: list[str] | tuple[str, ...] | None = None,
    ) -> time:
        """Encode a value into `time`.

        将值编码为 `time`。
        """
        return self.time.encode(value, formats=formats)

    def decode_datetime(
        self,
        value: datetime,
        timezone: str | ZoneInfo | None = None,
        *,
        target: DateTimeDecodeTarget | None = None,
        format: str | None = None,
    ) -> DateTimeOutput:
        """Decode `datetime` into an external representation.

        将 `datetime` 解码为外部表示。
        """
        return self.datetime.decode(
            value,
            timezone=timezone,
            target=target,
            format=format,
        )

    def decode_date(
        self,
        value: date,
        timezone: str | ZoneInfo | None = None,
        *,
        target: DateDecodeTarget | None = None,
        format: str | None = None,
        date_boundary_policy: DateBoundaryPolicy | None = None,
        timestamp_unit: TimestampUnit | None = None,
    ) -> DateOutput:
        """Decode `date` into an external representation.

        将 `date` 解码为外部表示。
        """
        return self.date.decode(
            value,
            timezone=timezone,
            target=target,
            format=format,
            date_boundary_policy=date_boundary_policy,
            timestamp_unit=timestamp_unit,
        )

    def decode_time(
        self,
        value: time,
        *,
        target: TimeDecodeTarget | None = None,
        format: str | None = None,
    ) -> TimeOutput:
        """Decode `time` into an external representation.

        将 `time` 解码为外部表示。
        """
        return self.time.decode(value, target=target, format=format)

    def encode(
        self,
        value: TemporalInput,
        timezone: str | ZoneInfo | None = None,
        *,
        prefer: str = "datetime",
    ) -> TemporalValue:
        """Encode a temporal value by inferring or using the preferred target type.

        通过推断或指定偏好的目标类型编码时间值。

        Args:
            value: Input temporal value.
                输入的时间值。
            timezone: Target timezone for `date` and `datetime` conversions.
                `date` 和 `datetime` 转换使用的目标时区。
            prefer: Preferred target type when the input is ambiguous. Supported values are
                `datetime`, `date`, and `time`.
                当输入存在歧义时偏好的目标类型。支持 `datetime`、`date` 和 `time`。
        """
        if prefer == "datetime":
            return self.encode_datetime(value, timezone=timezone)
        if prefer == "date":
            return self.encode_date(value, timezone=timezone)
        if prefer == "time":
            return self.encode_time(value)

        raise ValueError(f"Unsupported temporal encode preference: {prefer}.")

    def decode(
        self,
        value: TemporalValue,
        timezone: str | ZoneInfo | None = None,
        *,
        target: str | None = None,
        format: str | None = None,
    ) -> TemporalOutput:
        """Decode a temporal value by dispatching on its runtime type.

        根据运行时类型分发并解码时间值。
        """
        match value:
            case datetime():
                return self.decode_datetime(value, timezone=timezone, target=target, format=format)  # type: ignore[arg-type]
            case date():
                return self.decode_date(value, timezone=timezone, target=target, format=format)  # type: ignore[arg-type]
            case time():
                return self.decode_time(value, target=target, format=format)  # type: ignore[arg-type]
            case _:
                raise ValueError(f"Unsupported temporal value type: {type(value).__name__}.")


def parse_temporal(
    value: TemporalInput,
    timezone: str | ZoneInfo | None = None,
    *,
    options: TemporalCodecOptions | None = None,
    prefer: str = "datetime",
) -> TemporalValue:
    """Parse or normalize a value into a temporal object.

    将输入值解析或归一化为时间对象。
    """
    return TemporalCodec(options).encode(value, timezone=timezone, prefer=prefer)


def format_temporal(
    value: TemporalValue,
    timezone: str | ZoneInfo | None = None,
    *,
    options: TemporalCodecOptions | None = None,
    target: str | None = None,
    format: str | None = None,
) -> TemporalOutput:
    """Format a temporal object into an external representation.

    将时间对象格式化为外部表示。
    """
    return TemporalCodec(options).decode(
        value,
        timezone=timezone,
        target=target,
        format=format,
    )
