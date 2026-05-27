from matplotlib.axes import Axes

from athena_matplotlib.decorations import apply_cartesian_style
from athena_matplotlib.options import RenderFigureOptions
from athena_matplotlib.rendering.axes_runtime import resolve_axes_runtime
from athena_matplotlib.rendering.color_cycle import ColorCycle
from athena_matplotlib.rendering.plots.line_plot import LineArtist
from athena_matplotlib.rendering.render_plan import resolve_cartesian_render_plan
from athena_matplotlib.specs import ChartSpec


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
        # Render plan
        render_plan = resolve_cartesian_render_plan(chart)
        if render_plan.line_plots:
            for line_plot in render_plan.line_plots:
                self._line_artist.draw(
                    axes_runtime.axes_for_y_axis(line_plot.plot.y_axis_side),
                    line_plot,
                    options=options.line_plot,
                )
        if render_plan.bar_plots:
            pass

        # Legend

        # Tick
