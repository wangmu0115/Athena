import matplotlib.dates as mdates

from athena_kit.core.temporal.codec import TemporalCodec
from athena_kit.core.values.optional import optional_or_else
from athena_kit.matplotlib.specs.coords.tick import TickLabelFormatter
from athena_kit.matplotlib.types import AxisDataType, TickLabelFormatKind


def format_tick_label(
    value: object,
    formatter: TickLabelFormatter,
    *,
    axis_data_type: AxisDataType,
    temporal_codec: TemporalCodec | None = None,
) -> str:
    """格式化单个刻度标签。

    该函数只负责将刻度值转换为展示文本，不负责坐标轴数据归一化，也不负责构建具体绘图库的 Formatter 对象。

    Args:
        value: 待格式化的刻度值，通常是已经归一化后的 Python 值。
        label_format: 刻度格式化配置。
        axis_data_type: 坐标轴数据类型，用于在 `label_format.kind` 为 `auto` 时推断格式化方式。

    Returns:
        格式化后的刻度标签文本。

    Raises:
        ValueError: 当格式化类型不受支持时抛出。
    """
    if value is None:
        return ""

    temporal_codec = optional_or_else(temporal_codec, default_factory=TemporalCodec)

    kind = _resolve_tick_label_format_kind(formatter.kind, axis_data_type=axis_data_type)
    match kind:
        case "number":
            label = _format_number(value, formatter.precision)
        case "currency":
            label = _format_number(value, formatter.precision, grouping_separator=True)
        case "percent":
            label = _format_number(value, formatter.precision, scale=100.0)
        case "category":
            label = str(value)
        case "datetime":
            label = temporal_codec.format_datetime(
                mdates.num2date(value),
                output_format="formatted",
                format_pattern=formatter.datetime_format,
            )
        case "date":
            label = temporal_codec.format_date(
                mdates.num2date(value),
                output_format="formatted",
                format_pattern=formatter.date_format,
            )
        case "time":
            label = temporal_codec.format_time(
                mdates.num2date(value),
                output_format="formatted",
                format_pattern=formatter.time_format,
            )
        case _:
            raise ValueError(f"Unsupported tick formatter kind: {kind}.")

    return f"{formatter.prefix}{label}{formatter.suffix}"


def _format_number(
    value: object,
    precision: int | None = None,
    *,
    grouping_separator: bool = False,
    scale: float = 1.0,
) -> str:
    number = float(value) * scale

    if precision is None:
        return f"{number:g}"

    format = f",.{precision}f" if grouping_separator else f".{precision}f"
    return f"{number:{format}}"


def _resolve_tick_label_format_kind(kind: TickLabelFormatKind, *, axis_data_type: AxisDataType) -> TickLabelFormatKind:
    if kind == "auto":
        match axis_data_type:
            case "datetime" | "timestamp_s" | "timestamp_ms":
                return "datetime"
            case "date":
                return "date"
            case "time":
                return "time"
            case "number":
                return "number"
            case "category":
                return "category"
            case _:
                raise ValueError(f"Unsupported axis data type: {axis_data_type}.")
    return kind
