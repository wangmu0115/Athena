from matplotlib.axes import Axes

from athena_kit.matplotlib.decorations import apply_cartesian_style
from athena_kit.matplotlib.options import RenderFigureOptions
from athena_kit.matplotlib.rendering.color_cycle import ColorCycle
from athena_kit.matplotlib.rendering.coords._axes_runtime import AxesRuntime, build_axes_runtime
from athena_kit.matplotlib.rendering.coords._render_plan import AxisTickContext, resolve_cartesian_render_plan
from athena_kit.matplotlib.rendering.coords.legend import render_cartesian_legend
from athena_kit.matplotlib.rendering.coords.tick import render_axis_tick
from athena_kit.matplotlib.rendering.plots.bar_plot import BarArtist
from athena_kit.matplotlib.rendering.plots.line_plot import LineArtist
from athena_kit.matplotlib.specs import ChartSpec


class CartesianCoordRenderer:
    def __init__(self, color_cycle: ColorCycle):
        self._line_artist = LineArtist(color_cycle)
        self._bar_artist = BarArtist(color_cycle)

    def render(self, axes: Axes, chart: ChartSpec, *, options: RenderFigureOptions):
        # 1. 运行时 Axes 配置，根据 Y 轴的位置可能有两个 Axes
        axes_runtime: AxesRuntime = build_axes_runtime(axes, chart.coord)
        # 2. 轴线、轴标签、刻度和 Grid 渲染样式配置
        apply_cartesian_style(axes_runtime, chart.coord, options=options.cartesian)
        # 3. Plot artists
        if not chart.plots:
            return
        render_plan = resolve_cartesian_render_plan(chart)
        if render_plan.line_plots:
            for line_plot in render_plan.line_plots:
                self._line_artist.draw(
                    axes_runtime.axes_for_y_axis(line_plot.plot.y_axis_side),
                    line_plot,
                    options=options.line_plot,
                )
        if render_plan.bar_plots:
            self._bar_artist.draw(
                axes_runtime.axes_for_y_axis(render_plan.bar_plots.plots[0].y_axis_side),
                render_plan.bar_plots,
                # options
            )

        # 4. Tick
        x_tick_context = AxisTickContext(values=render_plan.x_values, positions=render_plan.x_positions)
        render_axis_tick(
            axes_runtime.primary.xaxis,
            chart.coord.x_axis,
            context=x_tick_context,
        )
        if axes_runtime.left_y is not None and chart.coord.left_y_axis is not None:
            render_axis_tick(axes_runtime.left_y.yaxis, chart.coord.left_y_axis)
        if axes_runtime.right_y is not None and chart.coord.right_y_axis is not None:
            render_axis_tick(axes_runtime.right_y.yaxis, chart.coord.right_y_axis)
        # 5. Legend
        render_cartesian_legend(
            axes_runtime,
            options=options.legend,
            override=chart.legend,
        )
