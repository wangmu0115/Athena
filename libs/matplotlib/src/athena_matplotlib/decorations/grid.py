from matplotlib.axes import Axes

import matplotlib as mpl
from athena_core.values.fallbacks import first_not_none
from athena_core.values.optional import safe_getattr
from athena_matplotlib.options.coords.grid import GridOptions


def apply_grid_style(axes: Axes, *, options: GridOptions | None, override: GridOptions | None):
    visible = first_not_none(
        safe_getattr(override, "visible"),
        safe_getattr(options, "visible"),
        default=mpl.rcParams["axes.grid"],
    )
    if not visible:
        axes.grid(False)
    else:
        style_params: dict[str, object] = {}
        if options is not None:
            style_params.update(options.model_dump(exclude_none=True, by_alias=True, exclude=["visible"]))
        if override is not None:
            style_params.update(override.model_dump(exclude_none=True, by_alias=True, exclude=["visible"]))

        axes.grid(True, **style_params)
