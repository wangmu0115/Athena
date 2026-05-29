from matplotlib.axes import Axes

from athena_core.values.fallbacks import first_non_empty
from athena_core.values.optional import safe_getattr
from athena_matplotlib.options import ChartOptions
from athena_matplotlib.specs import ChartSpec


def apply_chart_style(axes: Axes, chart: ChartSpec, *, options: ChartOptions | None = None):
    override = chart.options
    # 背景色
    facecolor = first_non_empty(
        safe_getattr(override, "facecolor"),
        safe_getattr(options, "facecolor"),
    )
    if facecolor:
        axes.set_facecolor(facecolor)
    # 标题
    if chart.title:
        style_params: dict[str, object] = {}
        if options is not None:
            style_params.update(options.model_dump(exclude_none=True, by_alias=True, exclude=["facecolor"]))
        if override is not None:
            style_params.update(override.model_dump(exclude_none=True, by_alias=True, exclude=["facecolor"]))
        # apply title and style
        axes.set_title(chart.title, **style_params)
