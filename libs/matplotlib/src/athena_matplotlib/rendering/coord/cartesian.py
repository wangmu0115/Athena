from dataclasses import dataclass
from typing import Literal

from matplotlib.axes import Axes

from athena_matplotlib.options.renderfig import RenderFigureOptions
from athena_matplotlib.rendering.base import ColorCycle
from athena_matplotlib.specs import ChartSpec
from athena_matplotlib.specs.coords import CartesianCoord


class CartesianCoordRenderer:
    def __init__(self, color_cycle: ColorCycle):
        # self._line_artist = LineArtist(color_cycle)
        pass

    def render(self, axes: Axes, chart: ChartSpec, *, options: RenderFigureOptions):
        # 运行时 Axes 配置，根据 Y 轴的位置可能有两个 Axes
        axes_runtime = resolve_axes_runtime(axes, chart.coord)
        # 轴线、轴标签、刻度和 Grid 渲染样式配置
        apply_coord_style(axes_runtime, chart.coord, default_options=default_options, override_options=override_options)
        # Plot artists
        render_plan = build_cartesian_render_plan(chart)
        if render_plan.line_plots:  # Line Plot
            for line_plot in render_plan.line_plots:
                self._line_artist.draw(
                    axes_runtime.axes_for_y_axis(line_plot.plot.y_axis_side),
                    line_plot,
                    default_options=default_options,
                    override_options=override_options,
                )
        if render_plan.bar_plot_group:  # Bar Plot
            pass
        # Legend


@dataclass
class AxesRuntime:
    primary: Axes
    left_y: Axes | None
    right_y: Axes | None

    def axes_for_y_axis(self, side: Literal["left", "right"]) -> Axes:
        if side == "left" and self.left_y is not None:
            return self.left_y
        if side == "right" and self.right_y is not None:
            return self.right_y
        raise ValueError(f"Plot requires {side} Y axis, but {side} Y axis is not configured.")


def resolve_axes_runtime(axes: Axes, coord: CartesianCoord) -> AxesRuntime:
    if coord.left_y_axis is not None and coord.right_y_axis is not None:
        axes_right = axes.twinx()
        return AxesRuntime(primary=axes, left_y=axes, right_y=axes_right)

    if coord.left_y_axis is not None:
        return AxesRuntime(primary=axes, left_y=axes, right_y=None)

    # Coord only has right Y, set primary axes to right Y.
    axes.yaxis.tick_right()
    axes.yaxis.set_label_position("right")
    return AxesRuntime(primary=axes, left_y=None, right_y=axes)
