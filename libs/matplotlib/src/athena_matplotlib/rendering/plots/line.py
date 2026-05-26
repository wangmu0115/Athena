from matplotlib.axes import Axes

from athena_charts_matplotlib.adapters.series import AlignedLinePlot
from athena_charts_matplotlib.rendering.options.base import ColorCycle
from athena_charts_matplotlib.rendering.options.chart import ChartOptions
from athena_charts_matplotlib.rendering.options.plot import LinePlotOptions
from athena_core.values.optional import optional_map_or, safe_getattr


class LineArtist:
    def __init__(self, color_cycle: ColorCycle):
        self._color_cycle = color_cycle

    def draw(
        self,
        axes: Axes,
        plot: AlignedLinePlot,
        *,
        options: LinePlotOptions | None,
    ) -> None:
        # 绘制折线图
        axes.plot(
            plot.x_values,
            plot.y_values,
            zorder=plot.plot.z_index,
            label=plot.plot.name,
            **self._resolve_plot_params(default_options=default_options, override_options=override_options),
        )
        # 数据标签

    def _resolve_plot_params(
        self,
        *,
        default_options: ChartOptions | None,
        override_options: ChartOptions | None,
    ) -> dict[str, object]:
        params: dict[str, object] = optional_map_or(
            safe_getattr(default_options, "line_plot"),
            lambda x: x.build_plot_params(),
            default={},
        )
        if override_options is not None:
            params.update(
                optional_map_or(
                    override_options.line_plot,
                    lambda x: x.build_plot_params(),
                    default={},
                )
            )
        if "color" not in params:
            linecolor = self._color_cycle.next()
            if linecolor:
                params["color"] = linecolor
        return params
