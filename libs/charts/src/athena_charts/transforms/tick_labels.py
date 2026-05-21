from athena_charts.specs.coords import AxisDataType, TickLabelFormat, TickLabelFormatKind
from athena_core.temporal.codec import TemporalCodec
from athena_core.values.optional import optional_or_else


def format_tick_label(
    value: object,
    label_format: TickLabelFormat,
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

    resolved_temporal_codec = optional_or_else(temporal_codec, default_factory=TemporalCodec)

    resolved_kind = _resolve_tick_label_format_kind(label_format.kind, axis_data_type=axis_data_type)
    match resolved_kind:
        case "number":
            label = _format_number(value, precision=label_format.precision)
        case "currency":
            label = _format_number(value, precision=label_format.precision, thousands_separator=True)
        case "percent":
            label = _format_number(value, precision=label_format.precision, scale=100.0)
        case "category":
            label = str(value)
        case "datetime":
            label = resolved_temporal_codec.format_datetime(
                value,
                output_format="formatted",
                format_pattern=label_format.datetime_format,
            )
        case "date":
            label = resolved_temporal_codec.format_date(
                value,
                output_format="formatted",
                format_pattern=label_format.date_format,
            )
        case "time":
            label = resolved_temporal_codec.format_time(
                value,
                output_format="formatted",
                format_pattern=label_format.time_format,
            )
        case _:
            raise ValueError(f"Unsupported tick formatter kind: {resolved_kind}.")

    return f"{label_format.prefix}{label}{label_format.suffix}"


def _format_number(
    value: object,
    *,
    precision: int | None = None,
    thousands_separator: bool = False,
    scale: float = 1.0,
) -> str:
    number = float(value) * scale
    if precision is None:
        return f"{number:g}"
    return f"{number:{',' if thousands_separator else ''}.{precision}f}"


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
