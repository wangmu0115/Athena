from matplotlib.axes import Axes

from athena_core.values.fallbacks import first_non_empty
from athena_core.values.optional import optional_map_or, safe_getattr
from athena_matplotlib.options import ChartOptions
from athena_matplotlib.specs import ChartSpec


def apply_chart_style(axes: Axes, chart: ChartSpec, *, options: ChartOptions):
    override = chart.chart_options
    # 背景色
    facecolor = first_non_empty(
        safe_getattr(override, "facecolor"),
        safe_getattr(options, "facecolor"),
    )
    if facecolor:
        axes.set_facecolor(facecolor)
    # 标题
    if chart.title:
        title_decoration_params: dict[str, object] = optional_map_or(
            options,
            lambda x: x.build_title_params(),
            default={},
        )
        if override:
            title_decoration_params.update(
                optional_map_or(
                    override,
                    lambda x: x.build_title_params(),
                    default={},
                )
            )
        axes.set_title(chart.title, **title_decoration_params)
