from typing import Literal

from matplotlib.axes import Axes

from athena_matplotlib.options.coords.axis import AxisOptions


def apply_axis_style(
    axes: Axes,
    loc: Literal["top", "bottom", "left", "right"],
    *,
    options: AxisOptions | None,
    override: AxisOptions | None,
):
    if options is None and override is None:
        return
    # Spine
    spine_style_params: dict[str, object] = {}
    if options is not None and options.spine is not None:
        spine_style_params.update(options.spine.model_dump(exclude_none=True, by_alias=True))
    if override is not None and override.spine is not None:
        spine_style_params.update(override.spine.model_dump(exclude_none=True, by_alias=True))
    axes.spines[loc].set(**spine_style_params)

    # Label
    label_style_params: dict[str, object] = {}
    if options is not None and options.label is not None:
        label_style_params.update(options.label.model_dump(exclude_none=True, by_alias=True))
    if override is not None and override.label is not None:
        label_style_params.update(override.label.model_dump(exclude_none=True, by_alias=True))
    if loc in {"top", "bottom"}:
        axes.xaxis.label.set(**label_style_params)
    if loc in {"left", "right"}:
        axes.yaxis.label.set(**label_style_params)
