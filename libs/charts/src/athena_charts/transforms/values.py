from datetime import date, datetime, time
from typing import Any

from athena_charts.specs.coords.axis import AxisSpec, TickFormatter


class AxisValueTransformer:
    """Engine-neutral transformation from raw values to semantic axis values.

    This layer belongs to ``athena-charts`` because timestamp/category/number/date
    normalization is part of the chart DSL semantics. Concrete engines may still
    adapt these normalized values to backend-specific representations.
    """

    def normalize(self, value: Any, axis: AxisSpec) -> Any:
        return normalize_axis_value(value, axis.data_type)

    def format(self, value: Any, axis: AxisSpec) -> str:
        return format_axis_value(value, axis.ticks.formatter, data_type=axis.data_type)


def normalize_axis_value(value: object, data_type: str) -> Any:
    if value is None:
        return None

    match data_type:
        case "timestamp_ms":
            return datetime.fromtimestamp(float(value) / 1000, tz=ZoneInfo(timezone))
        case "timestamp_s":
            return datetime.fromtimestamp(float(value), tz=ZoneInfo(timezone))
        case "datetime":
            if isinstance(value, datetime):
                return normalize_datetime_timezone(value, timezone)
            return normalize_datetime_timezone(datetime.fromisoformat(str(value)), timezone)
        case "date":
            if isinstance(value, date) and not isinstance(value, datetime):
                return value
            return date.fromisoformat(str(value))
        case "time":
            if isinstance(value, time):
                return value
            return time.fromisoformat(str(value))
        case "number":
            return float(value)
        case "category":
            return str(value)
        case _:
            raise ValueError(f"Unsupported axis data type: {data_type}.")

    if value is None:
        return None
    if data_type == "number":
        return float(value)
    if data_type == "category":
        return str(value)
    if data_type == "timestamp_ms":
        return datetime.fromtimestamp(float(value) / 1000)
    if data_type == "timestamp_s":
        return datetime.fromtimestamp(float(value))
    if data_type == "datetime":
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(str(value))
    if data_type == "date":
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        return date.fromisoformat(str(value))
    if data_type == "time":
        if isinstance(value, time):
            return value
        return time.fromisoformat(str(value))
    return value


def format_axis_value(value: Any, formatter: TickFormatter, *, data_type: str = "auto") -> str:
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
