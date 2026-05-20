from datetime import date, datetime, time

from athena_charts.specs.coords.axis import TickFormatter
from athena_charts.specs.coords.types import AxisDataType


def infer_tick_formatter_kind(axis_data_type: AxisDataType) -> ResolvedTickFormatterKind:
    """根据坐标轴数据类型推断默认刻度格式化类型。"""
    match axis_data_type:
        case "timestamp_ms" | "timestamp_s" | "datetime":
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
            raise ValueError(f"Unsupported axis data type: {axis_data_type!r}.")


def resolve_tick_formatter_kind(
    formatter: TickFormatter,
    *,
    axis_data_type: AxisDataType,
) -> ResolvedTickFormatterKind:
    """解析最终使用的刻度格式化类型。"""
    if formatter.kind == "auto":
        return infer_tick_formatter_kind(axis_data_type)
    return formatter.kind


def format_tick_label(
    value: object,
    formatter: TickFormatter,
    *,
    axis_data_type: AxisDataType,
) -> str:
    """格式化单个刻度标签。

    该函数只负责将刻度值转换为展示文本，不负责坐标轴数据归一化，
    也不负责构建具体绘图库的 Formatter 对象。

    Args:
        value: 待格式化的刻度值。通常是已经归一化后的 Python 值。
        formatter: 刻度格式化配置。
        axis_data_type: 坐标轴数据类型，用于在 ``formatter.kind`` 为 ``auto`` 时推断格式化方式。

    Returns:
        格式化后的刻度标签文本。

    Raises:
        ValueError: 当格式化类型不受支持时抛出。
    """
    if value is None:
        return ""

    kind = resolve_tick_formatter_kind(formatter, axis_data_type=axis_data_type)

    match kind:
        case "number":
            label = _format_number(value, precision=formatter.precision)

        case "percent":
            label = _format_percent(value, precision=formatter.precision)

        case "currency":
            label = _format_number(value, precision=formatter.precision)

        case "category":
            label = str(value)

        case "datetime":
            label = _format_datetime(value, formatter.datetime_format or "%Y-%m-%d %H:%M:%S")

        case "date":
            label = _format_date(value, formatter.datetime_format or "%Y-%m-%d")

        case "time":
            label = _format_time(value, formatter.datetime_format or "%H:%M:%S")

        case _:
            raise ValueError(f"Unsupported tick formatter kind: {kind!r}.")

    return f"{formatter.prefix}{label}{formatter.suffix}"


def _format_number(value: object, *, precision: int | None) -> str:
    number = float(value)
    if precision is None:
        return f"{number:g}"
    return f"{number:.{precision}f}"


def _format_percent(value: object, *, precision: int | None) -> str:
    number = float(value)
    resolved_precision = 0 if precision is None else precision
    return f"{number:.{resolved_precision}%}"


def _format_datetime(value: object, fmt: str) -> str:
    if isinstance(value, datetime):
        return value.strftime(fmt)

    if isinstance(value, date):
        return datetime.combine(value, time.min).strftime(fmt)

    raise ValueError(f"Expected datetime-like value, got {type(value).__name__}.")


def _format_date(value: object, fmt: str) -> str:
    if isinstance(value, datetime):
        return value.date().strftime(fmt)

    if isinstance(value, date):
        return value.strftime(fmt)

    raise ValueError(f"Expected date-like value, got {type(value).__name__}.")


def _format_time(value: object, fmt: str) -> str:
    if isinstance(value, datetime):
        return value.time().strftime(fmt)

    if isinstance(value, time):
        return value.strftime(fmt)

    raise ValueError(f"Expected time-like value, got {type(value).__name__}.")


def format_axis_value(
    value: object,
    formatter: TickFormatter,
    *,
    data_type: AxisDataType,
) -> str:
    kind = formatter.kind
    if kind == "auto":
        kind = data_type
    if value is None:
        return ""
    if kind in {"datetime", "date", "time"} and formatter.datetime_format and hasattr(value, "strftime"):
        return value.strftime(formatter.datetime_format)
    if kind == "percent":
        precision = 0 if formatter.precision is None else formatter.precision
        return f"{float(value) * 100:.{precision}f}%"
    if kind == "currency":
        precision = 2 if formatter.precision is None else formatter.precision
        return f"{formatter.prefix}{float(value):,.{precision}f}{formatter.suffix}"
    if kind == "number":
        if formatter.precision is None:
            body = f"{float(value):g}"
        else:
            body = f"{float(value):.{formatter.precision}f}"
        return f"{formatter.prefix}{body}{formatter.suffix}"
    return f"{formatter.prefix}{value}{formatter.suffix}"
