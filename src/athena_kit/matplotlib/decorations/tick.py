from typing import Literal

import matplotlib as mpl
from matplotlib.axes import Axes

from athena_kit.core.values.fallbacks import first_not_none
from athena_kit.core.values.optional import safe_getattr
from athena_kit.matplotlib.options.coords.tick import TickOptions


def apply_tick_style(
    axes: Axes,
    loc: Literal["top", "bottom", "left", "right"],
    *,
    options: TickOptions | None,
    override: TickOptions | None,
):
    if options is None and override is None:
        return

    axis = "x" if loc in {"top", "bottom"} else "y"
    line_visible = first_not_none(
        safe_getattr(safe_getattr(override, "line"), "visible"),
        safe_getattr(safe_getattr(options, "line"), "visible"),
        # xtick.top, xtick.bottom, ytick.left, ytick.right
        default=mpl.rcParams[f"{axis}tick.{loc}"],
    )
    label_visible = first_not_none(
        safe_getattr(safe_getattr(override, "label"), "visible"),
        safe_getattr(safe_getattr(options, "label"), "visible"),
        # xtick.labeltop, xtick.labelbottom, ytick.labelleft, ytick.labelright
        default=mpl.rcParams[f"{axis}tick.label{loc}"],
    )

    line_style_params: dict[str, object] = {}
    label_style_params: dict[str, object] = {}
    if options is not None:
        if options.line is not None:
            line_style_params.update(options.line.model_dump(exclude_none=True, by_alias=True, exclude=["visible"]))
        if options.label is not None:
            label_style_params.update(options.label.model_dump(exclude_none=True, by_alias=True, exclude=["visible"]))
    if override is not None:
        if override.line is not None:
            line_style_params.update(override.line.model_dump(exclude_none=True, by_alias=True, exclude=["visible"]))
        if override.label is not None:
            label_style_params.update(override.label.model_dump(exclude_none=True, by_alias=True, exclude=["visible"]))
    # Full Params
    params = {
        "axis": axis,
        f"{loc}": line_visible,
        f"label{loc}": label_visible,
    }
    if line_style_params:
        params.update(**line_style_params)
    if label_style_params:
        params.update(**label_style_params)
    # 更新 Tick 运行时渲染参数
    axes.tick_params(**params)
