from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from athena_kit.core.temporal.codec import TemporalCodec
from athena_kit.core.values.optional import optional_or_else
from athena_kit.matplotlib.datas import XYSeriesData
from athena_kit.matplotlib.specs.coords import AxisSpec, CartesianCoord
from athena_kit.matplotlib.specs.plots import BarPlot, LinePlot
from athena_kit.matplotlib.types import AxisDataType


@dataclass(slots=True)
class NormalizedXYSeries:
    """归一化后的 XY 系列数据"""

    x_values: list[Any]
    y_values: list[Any]


def normalize_lineplot_data(
    plot: LinePlot,
    coord: CartesianCoord,
    *,
    temporal_codec: TemporalCodec | None = None,
    skip_invalid: bool = True,
) -> NormalizedXYSeries:
    x_axis = coord.get_x_axis(plot.x_axis_side)
    y_axis = coord.get_y_axis(plot.y_axis_side)
    if x_axis is None or y_axis is None:
        raise ValueError(f"Coord doesn't has {plot.x_axis_side} or {plot.y_axis_side} axis.")

    return normalize_xy_series(
        plot.data.x,
        plot.data.y,
        x_axis=x_axis,
        y_axis=y_axis,
        temporal_codec=temporal_codec,
        skip_invalid=skip_invalid,
    )


def normalize_barplot_data(
    plot: BarPlot,
    coord: CartesianCoord,
    *,
    temporal_codec: TemporalCodec | None = None,
    skip_invalid: bool = True,
) -> NormalizedXYSeries:
    x_axis = coord.get_x_axis(plot.x_axis_side)
    y_axis = coord.get_y_axis(plot.y_axis_side)
    if x_axis is None or y_axis is None:
        raise ValueError(f"Coord doesn't has {plot.x_axis_side} or {plot.y_axis_side} axis.")
    raw_x_values = plot.data.x if isinstance(plot.data, XYSeriesData) else plot.data.categories
    raw_y_values = plot.data.y if isinstance(plot.data, XYSeriesData) else plot.data.values

    return normalize_xy_series(
        raw_x_values,
        raw_y_values,
        x_axis=x_axis,
        y_axis=y_axis,
        temporal_codec=temporal_codec,
        skip_invalid=skip_invalid,
    )


def normalize_xy_series(
    raw_x_values: Iterable[object],
    raw_y_values: Iterable[object],
    x_axis: AxisSpec,
    y_axis: AxisSpec,
    *,
    temporal_codec: TemporalCodec | None = None,
    skip_invalid: bool = True,
) -> NormalizedXYSeries:
    x_values: list[Any] = []
    y_values: list[Any] = []

    temporal_codec = optional_or_else(temporal_codec, default_factory=TemporalCodec)
    for raw_x, raw_y in zip(raw_x_values, raw_y_values, strict=True):
        try:
            x_values.append(normalize_axis_value(raw_x, x_axis.data_type, temporal_codec=temporal_codec))
            y_values.append(normalize_axis_value(raw_y, y_axis.data_type, temporal_codec=temporal_codec))
        except (TypeError, ValueError):
            if skip_invalid:
                continue
            raise

    return NormalizedXYSeries(x_values=x_values, y_values=y_values)


def normalize_axis_value(
    value: object,
    data_type: AxisDataType,
    *,
    temporal_codec: TemporalCodec | None = None,
) -> Any:
    """归一化单个坐标轴数据值，根据 `AxisDataType` 将原始值转换为渲染层更容易处理的标准 Python 类型。

    - timestamp_ms / timestamp_s / datetime 会转换为 `datetime`。
    - date 会转换为 `date`。
    - number 会转换为 `float`。
    - category 会转换为 `str`。
    - `None` 会保持为 `None`，用于表示缺失值。
    """
    if value is None:
        return None

    temporal_codec = optional_or_else(temporal_codec, default_factory=TemporalCodec)
    match data_type:
        case "timestamp_ms":
            return temporal_codec.parse_datetime(value, timestamp_unit="ms")
        case "timestamp_s":
            return temporal_codec.parse_datetime(value, timestamp_unit="s")
        case "datetime":
            return temporal_codec.parse_datetime(
                value,
                naive_datetime_policy="assume_timezone",
                boundary_policy="start",
            )
        case "date":
            if isinstance(value, datetime):
                return temporal_codec.parse_datetime(value).date()
            return temporal_codec.parse_date(value)
        case "number":
            return float(value)
        case "category":
            return str(value)
        case _:
            raise ValueError(f"Unsupported axis data type: {data_type}.")
