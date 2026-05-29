from athena_core.values.fallbacks import first_not_none
from athena_core.values.optional import safe_getattr
from athena_matplotlib.options.coords.legend import LegendOptions
from athena_matplotlib.rendering.coords._axes_runtime import AxesRuntime


def render_cartesian_legend(
    runtime: AxesRuntime,
    *,
    options: LegendOptions | None,
    override: LegendOptions | None,
):
    visible = first_not_none(
        safe_getattr(override, "visible"),
        safe_getattr(options, "visible"),
        default=True,
    )
    if not visible:
        return

    handles: list[object] = []
    labels: list[str] = []
    for axes in runtime.all_axes:
        axes_handles, axes_labels = axes.get_legend_handles_labels()
        for handle, label in zip(axes_handles, axes_labels, strict=True):
            if not label or label.startswith("_"):
                continue
            handles.append(handle)
            labels.append(label)
    if not handles:
        return

    style_params: dict[str, object] = {}
    if options is not None:
        style_params.update(options.model_dump(exclude_none=True, exclude=["visible"], by_alias=True))
    if override is not None:
        style_params.update(override.model_dump(exclude_none=True, exclude=["visible"], by_alias=True))
    # Apply legend and styles
    runtime.primary.legend(handles, labels, **style_params)
