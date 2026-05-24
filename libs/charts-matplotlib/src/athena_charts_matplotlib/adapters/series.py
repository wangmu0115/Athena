from dataclasses import dataclass

from athena_charts.specs.charts import ChartSpec
from athena_charts.specs.coords.cartesian import CartesianCoord
from athena_charts.specs.plots.bar import BarPlot
from athena_charts.specs.plots.line import LinePlot
from athena_charts.transforms.alignment import align_cartesian_plots_data


@dataclass
class AlignedLinePlot:
    plot: LinePlot
    index: int
    x_values: list[object]
    y_values: list[object]


@dataclass
class AlignedBarGroup:
    plots: list[BarPlot]
    y_values_list: list[list[object]]


@dataclass
class CartesianRenderPlan:
    x_values: list[object]
    line_plots: list[AlignedLinePlot]
    bar_plot_group: AlignedBarGroup


def build_cartesian_render_plan(chart: ChartSpec) -> CartesianRenderPlan:
    if not isinstance(chart.coord, CartesianCoord):
        raise ValueError("")

    missing_value = 0.0 if chart.bar_layout_mode == "stack" else None
    aligned_xy_series = align_cartesian_plots_data(
        chart.plots,
        chart.coord,
        missing_value=missing_value,
        category_order=chart.category_order,
    )

    line_plots: list[AlignedLinePlot] = []
    bar_plots: list[BarPlot] = []
    bar_plot_y_values_list: list[list[object]] = []
    for index, plot in chart.plots:
        if isinstance(plot, LinePlot):
            line_plots.append(AlignedLinePlot(plot=plot, y_values=aligned_xy_series.y_values_list[index]))
        elif isinstance(plot, BarPlot):
            bar_plots.append(plot)
            bar_plot_y_values_list.append(aligned_xy_series.y_values_list[index])

    return CartesianRenderPlan(
        x_values=aligned_xy_series.x_values,
        line_plots=line_plots,
        bar_plot_group=AlignedBarGroup(
            plots=bar_plots,
            y_values_list=bar_plot_y_values_list,
        ),
    )
