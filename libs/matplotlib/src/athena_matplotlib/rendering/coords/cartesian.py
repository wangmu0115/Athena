from matplotlib.axes import Axes

from athena_matplotlib.decorations import apply_cartesian_style
from athena_matplotlib.options import RenderFigureOptions
from athena_matplotlib.rendering.axes_runtime import resolve_axes_runtime
from athena_matplotlib.rendering.color_cycle import ColorCycle
from athena_matplotlib.rendering.coords.tick import render_axis_tick
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

        # Tick
        render_axis_tick(axes_runtime.primary.xaxis, chart.coord.x_axis)  # X
        if axes_runtime.left_y is not None and chart.coord.left_y_axis is not None:
            render_axis_tick(axes_runtime.left_y.yaxis, chart.coord.left_y_axis)
        if axes_runtime.right_y is not None and chart.coord.right_y_axis is not None:
            render_axis_tick(axes_runtime.right_y.yaxis, chart.coord.right_y_axis)  # X
        # Legend
        handles = []
        labels = []
        for ax in [axes_runtime.primary]:
            ax_handles, ax_labels = ax.get_legend_handles_labels()
            for handle, label in zip(ax_handles, ax_labels):
                if not label or label.startswith("_"):
                    continue
                handles.append(handle)
                labels.append(label)
        axes_runtime.primary.legend(
            handles,
            labels,
        )
