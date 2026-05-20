from collections.abc import Iterable
from datetime import datetime
from typing import Any

from athena_charts.specs.coords import AxisDataType
from athena_core.temporal.codec import TemporalCodec
from athena_core.values.optional import optional_or_else


def normalize_axis_values(
    values: Iterable[object],
    data_type: AxisDataType,
    *,
    temporal_codec: TemporalCodec | None = None,
) -> list[Any]:
    """批量归一化坐标轴数据，将一组原始坐标轴值按照指定的 `AxisDataType` 转换为渲染层更容易处理的标准 Python 类型。

    Args:
        values: 原始坐标轴值序列。
        data_type: 坐标轴数据类型。
        temporal_codec: 时间类型解析器。如果不传入，则使用默认 `TemporalCodec`。

    Returns:
        归一化后的坐标轴值列表。
    """
    resolved_temporal_codec = optional_or_else(temporal_codec, default_factory=TemporalCodec)
    return [
        normalize_axis_value(
            value,
            data_type,
            temporal_codec=resolved_temporal_codec,
        )
        for value in values
    ]


def normalize_axis_value(
    value: object,
    data_type: AxisDataType,
    *,
    temporal_codec: TemporalCodec | None = None,
) -> Any:
    """归一化单个坐标轴数据值，根据 `AxisDataType` 将原始值转换为渲染层更容易处理的标准 Python 类型。

    转换规则：
        - timestamp_ms / timestamp_s / datetime 会转换为 `datetime`。
        - date 会转换为 `date`。
        - time 会转换为 `time`。
        - number 会转换为 `float`。
        - category 会转换为 `str`。
        - `None` 会保持为 `None`，用于表示缺失值。

    Args:
        value: 原始坐标轴值。
        data_type: 坐标轴数据类型。
        temporal_codec: 时间类型解析器。如果不传入，则使用默认 `TemporalCodec`。

    Returns:
        归一化后的坐标轴值。

    Raises:
        ValueError: 当 `data_type` 不受支持时抛出。
    """
    if value is None:
        return None

    resolved_temporal_codec = optional_or_else(temporal_codec, default_factory=TemporalCodec)

    match data_type:
        case "timestamp_ms":
            return resolved_temporal_codec.parse_datetime(value, timestamp_unit="ms")
        case "timestamp_s":
            return resolved_temporal_codec.parse_datetime(value, timestamp_unit="s")
        case "datetime":
            return resolved_temporal_codec.parse_datetime(
                value,
                naive_datetime_policy="assume_timezone",
                boundary_policy="start",
            )
        case "date":
            if isinstance(value, datetime):
                return resolved_temporal_codec.parse_datetime(value).date()
            return resolved_temporal_codec.parse_date(value)
        case "time":
            return resolved_temporal_codec.parse_time(value)
        case "number":
            return float(value)
        case "category":
            return str(value)
        case _:
            raise ValueError(f"Unsupported axis data type: {data_type}.")
