from collections.abc import Sequence
from dataclasses import dataclass

import matplotlib.dates as mdates

from athena_kit.matplotlib.specs.chart import ChartSpec
from athena_kit.matplotlib.specs.coords import CartesianCoord
from athena_kit.matplotlib.specs.plots import BarPlot, LinePlot
from athena_kit.matplotlib.transforms.alignment_data import align_cartesian_plots_data
from athena_kit.matplotlib.types import BarLayoutMode
from athena_kit.matplotlib.types.specs import AxisDataType


@dataclass
class AlignedLinePlot:
    plot: LinePlot
    x_values: list[object]
    """原始 X 值，datetime/date/number/category"""
    x_positions: list[float]
    """Matplotlib 内部绘图坐标"""
    y_values: list[object]


@dataclass
class AlignedBarPlots:
    plots: list[BarPlot]
    x_values: list[object]
    """原始 X 值，datetime/date/number/category"""
    x_positions: list[float]
    """Matplotlib 内部绘图坐标"""
    y_values_list: list[list[object]]
    layout_mode: BarLayoutMode

    def __bool__(self) -> bool:
        return bool(self.plots)


@dataclass
class CartesianRenderPlan:
    x_values: list[object]
    """原始 X 值，datetime/date/number/category"""
    x_positions: list[float]
    """Matplotlib 内部绘图坐标"""
    line_plots: list[AlignedLinePlot]
    bar_plots: AlignedBarPlots


@dataclass
class AxisTickContext:
    """Axis tick 渲染上下文。

    values:
        原始 X 值，例如 `"A"`、`datetime(...)`、`1`。
    positions:
        Matplotlib 内部坐标，例如 `0.0`、`1.0`、`mdates.date2num(...)`。
    """

    values: list[object]
    positions: list[float]


def resolve_cartesian_render_plan(chart: ChartSpec) -> CartesianRenderPlan:
    if not isinstance(chart.coord, CartesianCoord):
        raise ValueError("Only Cartesian coord can build cartesian render plan.")

    # 对齐 X 轴时，缺省值
    missing_value = 0.0 if chart.bar_layout_mode == "stack" else None

    aligned_xy_series = align_cartesian_plots_data(
        chart.plots,
        chart.coord,
        missing_value=missing_value,
        category_order=chart.category_order,
    )

    x_positions = _resolve_x_positions(
        aligned_xy_series.x_values,
        chart.coord.x_axis.data_type,
    )

    line_plots: list[AlignedLinePlot] = []

    bar_plots: AlignedBarPlots = AlignedBarPlots(
        plots=[],
        x_values=aligned_xy_series.x_values,
        x_positions=x_positions,
        y_values_list=[],
        layout_mode=chart.bar_layout_mode,
    )

    for index, plot in enumerate(chart.plots):
        if isinstance(plot, LinePlot):
            line_plots.append(
                AlignedLinePlot(
                    plot=plot,
                    x_values=aligned_xy_series.x_values,
                    x_positions=x_positions,
                    y_values=aligned_xy_series.y_values_list[index],
                )
            )
        elif isinstance(plot, BarPlot):
            bar_plots.plots.append(plot)
            bar_plots.y_values_list.append(aligned_xy_series.y_values_list[index])

    return CartesianRenderPlan(
        x_values=aligned_xy_series.x_values,
        x_positions=x_positions,
        line_plots=line_plots,
        bar_plots=bar_plots,
    )


def _resolve_x_positions(x_values: Sequence[object], data_type: AxisDataType) -> list[float]:
    match data_type:
        case "category":
            return [float(i) for i in range(len(x_values))]
        case "number":
            return [float(x) for x in x_values]
        case "date" | "datetime" | "timestamp_ms" | "timestamp_s":
            return [mdates.date2num(x) for x in x_values]
        case _:
            raise ValueError(f"Unsupported x axis data type: {data_type}.")
