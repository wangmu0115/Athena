from dataclasses import dataclass

from matplotlib.axes import Axes

from athena_matplotlib.decorations import apply_cartesian_style
from athena_matplotlib.options import RenderFigureOptions
from athena_matplotlib.rendering.base import ColorCycle
from athena_matplotlib.rendering.coords.axes_runtime import resolve_axes_runtime
from athena_matplotlib.rendering.plots.line import LineArtist
from athena_matplotlib.specs import ChartSpec
from athena_matplotlib.specs.coords import CartesianCoord
from athena_matplotlib.specs.plots import BarPlot, LinePlot
from athena_matplotlib.transforms.alignment_data import align_cartesian_plots_data
from athena_matplotlib.types import BarLayoutMode


class CartesianCoordRenderer:
    def __init__(self, color_cycle: ColorCycle):
        self._line_artist = LineArtist(color_cycle)

    def render(self, axes: Axes, chart: ChartSpec, *, options: RenderFigureOptions):
        # 运行时 Axes 配置，根据 Y 轴的位置可能有两个 Axes
        axes_runtime = resolve_axes_runtime(axes, chart.coord)
        # 轴线、轴标签、刻度和 Grid 渲染样式配置
        apply_cartesian_style(axes_runtime, chart.coord, options=options)
        # Plot artists
        if not chart.plots:
            return
        render_plan = build_cartesian_render_plan(chart)
        if render_plan.line_plots:
            for line_plot in render_plan.line_plots:
                self._line_artist.draw(
                    axes_runtime.axes_for_y_axis(line_plot.plot.y_axis_side),
                    line_plot,
                )

        # render_plan = build_cartesian_render_plan(chart)
        # if render_plan.line_plots:  # Line Plot
        #     for line_plot in render_plan.line_plots:
        #         self._line_artist.draw(
        #             axes_runtime.axes_for_y_axis(line_plot.plot.y_axis_side),
        #             line_plot,
        #             default_options=default_options,
        #             override_options=override_options,
        #         )
        # if render_plan.bar_plot_group:  # Bar Plot
        #     pass
        # Legend


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


def build_cartesian_render_plan(chart: ChartSpec) -> CartesianRenderPlan:
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
