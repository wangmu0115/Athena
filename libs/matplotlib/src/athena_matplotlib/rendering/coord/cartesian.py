from matplotlib.axes import Axes

from athena_matplotlib.decorations import apply_cartesian_style
from athena_matplotlib.options.renderfig import RenderFigureOptions
from athena_matplotlib.rendering.base import ColorCycle
from athena_matplotlib.rendering.coord.axes_runtime import resolve_axes_runtime
from athena_matplotlib.specs import ChartSpec


class CartesianCoordRenderer:
    def __init__(self, color_cycle: ColorCycle):
        # self._line_artist = LineArtist(color_cycle)
        pass

    def render(self, axes: Axes, chart: ChartSpec, *, options: RenderFigureOptions):
        # 运行时 Axes 配置，根据 Y 轴的位置可能有两个 Axes
        axes_runtime = resolve_axes_runtime(axes, chart.coord)
        # 轴线、轴标签、刻度和 Grid 渲染样式配置
        apply_cartesian_style(axes_runtime, chart.coord, options=options)
        # Plot artists
        if not chart.plots:
            return

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
