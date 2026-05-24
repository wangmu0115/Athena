from typing import Literal

from matplotlib.axes import Axes

from athena_charts_matplotlib.rendering.options.chart import ChartOptions
from athena_core.values.optional import optional_map_or


def _apply_grid(axes: Axes, *, default_options: ChartOptions | None, override_options: ChartOptions | None):
    grid_params = optional_map_or(default_options, lambda x: x.build_grid_params, default={})
    if override_options is not None:
        grid_params.update(override_options.build_grid_params())
    # apply Grid params
    axes.grid(grid_params)


def _apply_axes_spine(
    axes: Axes,
    loc: Literal["top", "bottom", "left", "right"],
    *,
    default_options: ChartOptions | None,
    override_options: ChartOptions | None,
):
    pass
