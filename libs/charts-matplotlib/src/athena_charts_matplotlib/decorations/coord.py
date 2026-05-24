from typing import Literal

import matplotlib as mpl
from matplotlib.axes import Axes

from athena_charts_matplotlib.rendering.options.chart import ChartOptions
from athena_charts_matplotlib.rendering.options.coord import AxisOptions
from athena_core.values.fallbacks import first_not_none
from athena_core.values.optional import optional_map, safe_getattr


def apply_axes(
    axes: Axes,
    loc: Literal["top", "bottom", "left", "right"],
    *,
    default_options: ChartOptions | None,
    override_options: ChartOptions | None,
):
    pass


def apply_axis(
    axes: Axes,
    loc: Literal["top", "bottom", "left", "right"],
    label: str | None,
    *,
    default_options: AxisOptions | None,
    override_options: AxisOptions | None,
) -> bool:
    # Spine
    visible = first_not_none(
        safe_getattr(default_options, "visible"),
        safe_getattr(override_options, "visible"),
        mpl.rcParams[f"axes.spines.{loc}"],
    )
    axes.spines[loc].set_visible(visible)
    if visible:
        spine_params = optional_map(default_options, lambda x: x.build_spine_params)
        spine_params.update(optional_map(override_options, lambda x: x.build_spine_params))
        if spine_params:
            axes.spines[loc].set(**spine_params)
    # Axis label
    if label:
        axes.set_xlabel()



    return visible
