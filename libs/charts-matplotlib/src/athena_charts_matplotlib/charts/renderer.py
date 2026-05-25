from matplotlib.axes import Axes

from athena_charts.specs.charts import ChartSpec
from athena_charts.specs.coords import CartesianCoord
from athena_charts_matplotlib.coords.cartesian import CartesianCoordRenderer
from athena_charts_matplotlib.rendering.options import MatplotlibRenderOptions
from athena_charts_matplotlib.rendering.options.base import ColorCycle
from athena_charts_matplotlib.rendering.options.chart import ChartOptions
from athena_core.values.fallbacks import first_non_empty
from athena_core.values.optional import optional_map_or, safe_getattr


class ChartRenderer:
    def __init__(self, color_cycle: ColorCycle):
        self._cartesian_renderer = CartesianCoordRenderer(color_cycle)

    def render(self, axes: Axes, chart: ChartSpec, *, index: int, options: MatplotlibRenderOptions):
        override_chart_options = options.chart_overrides.get(index)
        # Chart facecolor
        facecolor = first_non_empty(
            safe_getattr(override_chart_options, "facecolor"),
            safe_getattr(options.chart_default, "facecolor"),
        )
        if facecolor:
            axes.set_facecolor(facecolor)
        # Chart title
        self._apply_title(
            axes,
            safe_getattr(chart.labels, "title"),
            default_options=options.chart_default,
            override_options=override_chart_options,
        )
        # Chart coord and plots
        if isinstance(chart.coord, CartesianCoord):
            self._cartesian_renderer.render(
                axes,
                chart,
                default_options=options.chart_default,
                override_options=override_chart_options,
            )

    def _apply_title(
        self,
        axes: Axes,
        title: str | None,
        *,
        default_options: ChartOptions,
        override_options: ChartOptions,
    ):
        if not title:
            return
        title_params = optional_map_or(default_options, lambda x: x.build_title_params(), default={})
        if override_options is not None:
            title_params.update(optional_map_or(override_options, lambda x: x.build_title_params(), default={}))
        axes.set_title(title, **title_params)
