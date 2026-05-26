from dataclasses import dataclass

from athena_matplotlib.specs.chart import ChartSpec
from athena_matplotlib.specs.coords import CartesianCoord
from athena_matplotlib.specs.plots import BarPlot, LinePlot
from athena_matplotlib.transforms.alignment_data import align_cartesian_plots_data
from athena_matplotlib.types import BarLayoutMode


@dataclass
class AlignedLinePlot:
    plot: LinePlot
    x_values: list[object]
    y_values: list[object]


@dataclass
class AlignedBarPlots:
    plots: list[BarPlot]
    x_values: list[object]
    y_values_list: list[list[object]]
    layout_model: BarLayoutMode


@dataclass
class CartesianRenderPlan:
    x_values: list[object]
    line_plots: list[AlignedLinePlot]
    bar_plots: AlignedBarPlots


def resolve_cartesian_render_plan(chart: ChartSpec) -> CartesianRenderPlan:
    if not isinstance(chart.coord, CartesianCoord):
        raise ValueError("Only Cartesian coord can build cartesian render plan.")

    # 对齐 X 轴时，缺省值
    missing_value = 0.0 if chart.bar_layout_model == "stack" else None

    aligned_xy_series = align_cartesian_plots_data(
        chart.plots,
        chart.coord,
        missing_value=missing_value,
        category_order=chart.category_order,
    )

    line_plots: list[AlignedLinePlot] = []
    bar_plots: AlignedBarPlots = AlignedBarPlots(
        plots=[],
        x_values=aligned_xy_series.x_values,
        y_values_list=[],
        layout_model=chart.bar_layout_model,
    )
    for index, plot in enumerate(chart.plots):
        if isinstance(plot, LinePlot):
            line_plots.append(
                AlignedLinePlot(
                    plot=plot,
                    x_values=aligned_xy_series.x_values,
                    y_values=aligned_xy_series.y_values_list[index],
                )
            )
        elif isinstance(plot, BarPlot):
            bar_plots.plots.append(plot)
            bar_plots.y_values_list.append(aligned_xy_series.y_values_list[index])

    return CartesianRenderPlan(
        x_values=aligned_xy_series.x_values,
        line_plots=line_plots,
        bar_plots=bar_plots,
    )
